""" Chroma DB Controller """

import chromadb
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from tqdm import tqdm
import json
from src.encoder import average_pool

def _split_chunk(lst, n_size):
    for i in range(0, len(lst), n_size):
        yield lst[i:i+n_size]

class Chroma:
    
    def __init__(self, collection_name = None):
        """ 크로마 DB 접속(docker container) """
        self.client = chromadb.HttpClient(host="localhost", port=8000)
        if collection_name:
            self.collection_name = collection_name
        
    def create_collection(self, collection_name = None):
        """ collection 생성 """
        self.client.create_collection(
            name = collection_name if collection_name else self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_collection(self, collection_name = None):
        """ collection use """
        self.collection = self.client.get_collection(name = collection_name if collection_name else self.collection_name)
        return self.collection

    def get_or_create_collection(self, collection_name = None):
        """ collection use """
        self.collection = self.client.get_or_create_collection(name = collection_name if collection_name else self.collection_name)
        return self.collection
    
    def delete_collection(self, collection_name = None):
        """ delete collection """
        self.client.delete_collection(name = collection_name if collection_name else self.collection_name)
    
    
    def upsert(self, documents, ids, metadatas, embeddings, **kwargs):
        """ data upsert """
        collection = self.get_collection(self.collection_name)
        collection.upsert(
            documents = documents,
            ids = ids,
            metadatas = metadatas,
            embeddings = embeddings,
            **kwargs
        )
        print(f"Upserted # of {len(documents)}Documents.")

        
    def batch_file_upsert(self, file_name: str):
        """ json 파일로 batch upsert """

        if isinstance(file_name, str):
            with open(file_name, "r") as f:
                data = json.load(f)
        else:
            data = file_name
        
        def _parallel_add_documents(data):
            documents = "###" + data['title'] + "\n" + data['text']
            data.update({"documents": documents})
            return data

        with ThreadPoolExecutor(cpu_count() - 3) as p:
            processed_data = list(tqdm(p.map(_parallel_add_documents, data)))

        splitted = _split_chunk(processed_data, 128)
        splitted = list(splitted)
        size = len(splitted)

        for idx in tqdm(range(size)):
            embed = average_pool([ele['documents'] for ele in splitted[idx]]).tolist()
        
            collection = self.get_collection(self.collection_name)
            collection.upsert(
                documents=[ele['documents'] for ele in splitted[idx]],
                ids=[ele['title'] for ele in splitted[idx]],
                metadatas=[{"url": ele['url']} for ele in splitted[idx]],
                embeddings=embed
            )

            print(f"Upserted # of {size}Documents.")
        
        
    def query(self, query_embeddings, n_results=5):
        """ 조회하기 """
        collection = self.get_collection(self.collection_name)
        return collection.query(query_embeddings=query_embeddings, n_results=n_results)

    def query_by_embedding(self, query, n_results=5):
        """ 조회하기 """
        query_embeddings = average_pool(query).tolist()
        collection = self.get_collection(self.collection_name)
        return collection.query(query_embeddings=query_embeddings, n_results=n_results)

    def __repr__(self):
        return f"Collections List:\n{self.client.list_collections()}"

    def __getitem__(self, key):
        return self.client.get_collection(key)
        
        
        
        
        
        