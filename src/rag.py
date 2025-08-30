from groq import Groq
import os
from typing import List, Dict, Any, Optional
from .embeddings import EmbeddingsManager
from .utils import logger

class SmartAPIAssistant:
    def __init__(self):
        self.embeddings_manager = EmbeddingsManager()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt = self.system_prompt = """You are RAGify, an advanced API Documentation Explorer using retrieval-augmented generation. Help developers with clear, practical guidance.

Guidelines:
- Base answers on provided documentation
- Include code examples when available  
- Be concise but comprehensive
- Focus on practical implementation
- If unsure, say so clearly"""
    
    def generate_response(self, query: str, docs: List[Dict], history: Optional[List] = None) -> str:
        context = self._prepare_context(docs)
        
        messages = [{"role": "system", "content": self.system_prompt}]
        if history: messages.extend(history[-4:])
        
        messages.append({
            "role": "user", 
            "content": f"Question: {query}\n\nDocumentation:\n{context}\n\nAnswer based on the documentation:"
        })
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _prepare_context(self, docs: List[Dict]) -> str:
        if not docs: return "No relevant documentation found."
        
        context = []
        for i, doc in enumerate(docs[:3], 1):
            content = doc.get('content', '')[:400]
            source = doc.get('metadata', {}).get('source', 'Unknown')
            url = doc.get('metadata', {}).get('url', '')
            context.append(f"Source {i} ({source}):\nURL: {url}\nContent: {content}\n")
        
        return "\n".join(context)
    
    def search_and_respond(self, query: str, history: Optional[List] = None) -> Dict[str, Any]:
        docs = self.embeddings_manager.search_similar(query, n_results=5)
        
        if not docs:
            return {
                "response": "No relevant documentation found. Please load the documentation first.",
                "sources": []
            }
        
        response = self.generate_response(query, docs, history)
        
        sources = []
        for doc in docs[:3]:
            meta = doc.get('metadata', {})
            sources.append({
                "source": meta.get('source', 'Unknown'),
                "url": meta.get('url', ''),
                "title": meta.get('title', ''),
                "similarity": round(doc.get('similarity', 0), 3)
            })
        
        return {"response": response, "sources": sources}