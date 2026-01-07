
import sys
import os
import uuid
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.getcwd())
load_dotenv()

from ai_agent.rag.retriever import RAGRetriever, Document

def seed_rich_data():
    print("Seeding RAG with Rich Persona Data...")
    
    try:
        retriever = RAGRetriever()
        patient_id = "7a5c5780-8e97-4e90-be2f-11c2545a4640" # Matching the E2E demo ID
        
        facts = [
            # Family & Relationships
            "My husband, Arthur, passed away three years ago in 2023. I miss him dearly every day.",
            "I have two children: Sarah, who lives in London, and Michael, who lives nearby in Shanghai.",
            "Sarah is a lawyer and calls me every Sunday evening.",
            "Michael is an architect and visits me on Tuesdays with my grandson, Leo.",
            "My grandson Leo operates a small bakery toy set I gave him.",
            
            # Personal History & Triggers
            "I used to teach History at the University of Shanghai for 40 years.",
            "I love classical music, especially Chopin. It calms me down when I am anxious.",
            "I am terrified of thunderstorms. They make me feel unsafe.",
            "The lake house keys are kept in the small blue porcelain bowl on the hallway console table.",
            "I often forget where I put my reading glasses; they are usually on the chain around my neck or on the kitchen counter.",
            
            # Preferences
            "I take my blue heart medication at 8 AM with breakfast.",
            "I prefer tea over coffee, specifically Jasmine tea.",
            "My favorite color is lilac.",
            "I do not like it when people speak too loudly; it confuses me."
        ]
        
        documents = []
        for fact in facts:
            doc = Document(
                id=str(uuid.uuid4()),
                text=fact,
                metadata={
                    "patient_id": patient_id, 
                    "category": "biography",
                    "timestamp": "2026-01-01T12:00:00"
                }
            )
            documents.append(doc)
            
        retriever.add_documents(documents)
        print("Success! Added detailed memories for Alice.")
        print(f"   Patient ID: {patient_id}")
        
    except Exception as e:
        print(f"Error seeding RAG: {e}")

if __name__ == "__main__":
    seed_rich_data()
