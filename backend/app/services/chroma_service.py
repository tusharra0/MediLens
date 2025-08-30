import chromadb
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

# ChromaDB client setup
client = chromadb.HttpClient(
    ssl=True,
    host='api.trychroma.com',
    tenant='c62ca6f6-ebde-4f3e-a727-885904e35df1',
    database='MediLens',
    headers={
        'x-chroma-token': 'ck-DhNfVgeXRLgL42wfYfSzqBbBs89Mbzp3gE4SCKrwX3as'
    }
)

# Get the collection
collection = client.get_collection(name="medical")

# Embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def query_collection(question, n_results=3, distance_threshold=1.5):
    """
    Query the ChromaDB collection with a question.
    Returns relevant documents based on similarity.
    """
    try:
        print(f"Querying ChromaDB with question: {question}")
        
        # Generate embedding for the question
        question_embedding = embedding_model.encode(question).tolist()
        print(f"Generated embedding with {len(question_embedding)} dimensions")
        
        # Query the collection
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=n_results
        )
        
        print(f"Raw ChromaDB results: {results}")
        
        # Filter out results with high distances (low similarity)
        filtered_documents = []
        filtered_distances = []
        
        if results['distances'] and len(results['distances']) > 0:
            for i, distance in enumerate(results['distances'][0]):
                if distance < distance_threshold:
                    filtered_documents.append(results['documents'][0][i])
                    filtered_distances.append(distance)
                    print(f"Accepted document {i} with distance {distance}")
                else:
                    print(f"Rejected document {i} with distance {distance} (threshold: {distance_threshold})")
        
        final_results = {
            'documents': [filtered_documents] if filtered_documents else [[]],
            'distances': [filtered_distances] if filtered_distances else [[]]
        }
        
        print(f"Filtered results: {len(filtered_documents)} documents")
        return final_results
        
    except Exception as e:
        print(f"Error in query_collection: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return empty results on error
        return {
            'documents': [[]],
            'distances': [[]]
        }

def add_document_to_collection(doc_id, text):
    """
    Add a document to the ChromaDB collection.
    """
    try:
        collection.add(
            ids=[doc_id],
            documents=[text]
        )
        print(f"Added document {doc_id} to collection")
        return True
    except Exception as e:
        print(f"Error adding document to collection: {str(e)}")
        return False