"""
RATIONALE:
Implements real RAG using:
1. Google Generative AI for Embeddings (models/embedding-001).
2. ChromaDB for local vector storage.
Adheres to RAG_CONTRACT.md.
"""

import os
import chromadb
from typing import List, Optional, Dict
from pydantic import BaseModel
import google.generativeai as genai

# Models
class Document(BaseModel):
    id: str
    text: str
    metadata: Dict

class RAGRetriever:
    def __init__(self, persistence_path: str = "./chroma_db"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize ChromaDB (Persistent)
        self.client = chromadb.PersistentClient(path=persistence_path)
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(name="memo_knowledge_base")

    def _embed_text(self, text: str) -> List[float]:
        """
        Generates embeddings using Google's embedding-001 model.
        """
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

    def add_documents(self, documents: List[Document]):
        """
        Adds documents to the Vector Store.
        """
        ids = [doc.id for doc in documents]
        texts = [doc.text for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Batch embed (Google supports batching, but doing simple loop for safety/clarity here)
        # Optimization: Use batch API if volume is high
        embeddings = [self._embed_text(text) for text in texts]
        
        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )
        print(f"✅ [RAG] Indexed {len(documents)} documents.")

    def retrieve(self, patient_id: str, query: str, limit: int = 5) -> List[Document]:
        """
        Retrieves semantic documents relevant to the query.
        Filters by `patient_id` in metadata.
        """
        query_embedding = self._embed_text(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"patient_id": patient_id} # Metadata filter
        )
        
        # Parse Chroma Results
        docs = []
        if results and results['ids']:
            # Chroma returns lists of lists
            ids = results['ids'][0]
            texts = results['documents'][0]
            metas = results['metadatas'][0]
            
            for i in range(len(ids)):
                docs.append(Document(
                    id=ids[i],
                    text=texts[i],
                    metadata=metas[i]
                ))
                
        print(f"🔍 [RAG] Retrieved {len(docs)} docs for query: '{query}'")
        return docs

# Quick Test/Seed if run directly
if __name__ == "__main__":
    try:
        retriever = RAGRetriever()
        
        # Seed some data
        docs = [
            Document(id="1", text="Patient loves gardening.", metadata={"patient_id": "p1", "category": "hobby"}),
            Document(id="2", text="Patient needs meds at 8am.", metadata={"patient_id": "p1", "category": "medical"}),
            Document(id="3", text="Patient lives in Shanghai.", metadata={"patient_id": "p2", "category": "bio"}),
        ]
        retriever.add_documents(docs)
        
        # Test Retrieve
        results = retriever.retrieve("p1", "What does he like?")
        for r in results:
            print(f" - {r.text}")
            
    except Exception as e:
        print(f"Error: {e}")
