""" Chroma DB Controller """

import chromadb

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

        
#     def batch_upsert(self, documents, ids, metadatas, embeddings, **kwargs):
#         """ data upsert """
        
#         def _parallel_processing(data):
#             documents = "###" + data['title'] + "\n" + data['text']
#             data.update({"documents": documents})
#             return data
        
#         with Pool(cpu_count()-2) as p:
#             embeddings = list(tqdm(p.imap(_parallel_processing, data)))
#         return embeddings
        
        collection = self.get_collection(self.collection_name)
        collection.upsert(
            documents = documents,
            ids = ids,
            metadatas = metadatas,
            embeddings = embeddings,
            **kwargs
        )
        print(f"Upserted # of {len(documents)}Documents.")
        
        
    def query(self, query_embeddings, n_results=5):
        """ 조회하기 """
        collection = self.get_collection(self.collection_name)
        return collection.query(query_embeddings=query_embeddings, n_results=n_results)

    def __repr__(self):
        return f"Collections List:\n{self.client.list_collections()}"

    def __getitem__(self, key):
        return self.client.get_collection(key)
        
        
        
        
        
        