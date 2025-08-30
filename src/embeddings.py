import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import uuid
from .utils import logger, chunk_text

class EmbeddingsManager:
    def __init__(self, collection_name: str = "api_docs"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Use in-memory client for hosting compatibility
        try:
            # Try persistent client first (for local development)
            self.client = chromadb.PersistentClient(path="./chroma_db")
        except Exception as e:
            logger.warning(f"Persistent client failed ({e}), using in-memory client")
            # Fallback to in-memory client for hosting environments
            self.client = chromadb.Client()
        
        self.collection = self._get_collection(collection_name)
        logger.info(f"Initialized embeddings with {collection_name}")
    
    def _get_collection(self, name: str):
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(name)
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
    
    def add_documents(self, docs: List[Dict[str, Any]]) -> int:
        documents, metadatas, ids = [], [], []
        
        for doc in docs:
            if 'error' in doc: continue
            
            chunks = chunk_text(doc.get('content', ''), 800, 100)
            for i, chunk in enumerate(chunks):
                if not chunk.strip(): continue
                
                documents.append(f"Title: {doc.get('title', '')}\n\nContent: {chunk}")
                metadatas.append({
                    "source": doc.get('source', 'Unknown'),
                    "url": doc.get('url', ''),
                    "title": doc.get('title', ''),
                    "chunk_index": i
                })
                ids.append(str(uuid.uuid4()))
        
        if not documents: return 0
        
        # Process in batches
        batch_size = 50
        total = 0
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            embeddings = self.create_embeddings(batch_docs)
            self.collection.add(
                documents=batch_docs,
                embeddings=embeddings,
                metadatas=batch_meta,
                ids=batch_ids
            )
            total += len(batch_docs)
        
        return total
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.create_embeddings([query])[0]
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            formatted = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "similarity": 1 - results['distances'][0][i]
                    })
            return formatted
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        try:
            return {"total_documents": self.collection.count()}
        except:
            return {"total_documents": 0}