import chromadb

class Chroma:
    
    def __init__(self, collection_name = None):
        self.client = chromadb.HttpClient(host="localhost", port=8000)
        if collection_name:
            self.collection_name = collection_name
        
    def create_collection(self, collection_name = None):
        self.client.create_collection(
            name = collection_name if collection_name else self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_collection(self, collection_name = None):
        self.collection = self.client.get_collection(name = collection_name if collection_name else self.collection_name)
        return self.collection
    
    def delete_collection(self, collection_name = None):
        self.client.delete_collection(name = collection_name if collection_name else self.collection_name)
    
    
    def upsert(self, documents, ids, uris, embeddings):
        collection = self.get_collection(self.collection_name)
        collection.upsert(
            documents = documents,
            ids = ids,
            uris = uris,
            embeddings = embeddings
        )
        print(f"Upserted # of {len(documents)}Documents.")
        
    def query(self, query_embeddings, n_results=5):
        collection = self.get_collection(self.collection_name)
        return collection.query(query_embeddings=query_embeddings, n_results=5)
        
        
        
        
        
        