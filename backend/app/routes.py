from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2
import sqlite3
import chromadb
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from services.rag_service import generate_answer
from services.chroma_service import query_collection, add_document_to_collection

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_NAME = "MediLens.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content_type TEXT NOT NULL,
            data BLOB NOT NULL,
            size INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def extract_text_from_pdf(file_stream):
    """Extract text from PDF."""
    file_stream.seek(0)
    reader = PdfReader(file_stream)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        print("=== PDF Upload Started ===")
        
        if 'pdf' not in request.files:
            print("Error: No file provided")
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['pdf']
        print(f"Received file: {file.filename}")
        
        file_data = file.read()
        file_size = len(file_data)
        print(f"File size: {file_size} bytes")

        # Save PDF in SQLite
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pdf_files (filename, content_type, data, size)
            VALUES (?, ?, ?, ?)
        """, (file.filename, file.content_type, file_data, file_size))
        pdf_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"Saved PDF with ID: {pdf_id}")

        # Extract text
        file.stream.seek(0)
        pdf_text = extract_text_from_pdf(file.stream)
        print(f"Extracted text length: {len(pdf_text)} characters")

        if pdf_text.strip():
            # Chunk the text
            chunks = chunk_text(pdf_text, chunk_size=1000, overlap=200)
            print(f"Created {len(chunks)} chunks")
            
            # Add chunks to ChromaDB
            chunks_added = 0
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file.filename}_{pdf_id}_{i}"
                if add_document_to_collection(chunk_id, chunk):
                    chunks_added += 1
                    
            print(f"Added {chunks_added} chunks to ChromaDB")

            return jsonify({
                "message": "File processed successfully",
                "filename": file.filename,
                "size": file_size,
                "chunks_created": len(chunks),
                "chunks_added_to_db": chunks_added
            }), 200
        else:
            print("Warning: No extractable text from PDF")
            return jsonify({
                "message": "File saved, but no extractable text",
                "filename": file.filename,
                "size": file_size
            }), 200

    except Exception as e:
        print(f"Error in upload_pdf: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        print("=== Question Processing Started ===")
        
        data = request.json
        question = data.get("question")
        print(f"Received question: {question}")

        if not question:
            print("Error: No question provided")
            return jsonify({"error": "No question provided"}), 400

        # Query ChromaDB
        print("Querying ChromaDB...")
        results = query_collection(question, n_results=5)
        
        # Extract documents
        retrieved_chunks = []
        if results.get("documents") and len(results["documents"]) > 0:
            retrieved_chunks = results["documents"][0]
        
        print(f"Retrieved {len(retrieved_chunks)} chunks from ChromaDB")
        
        if not retrieved_chunks:
            print("Warning: No relevant documents found")
            return jsonify({
                "question": question,
                "answer": "I couldn't find any relevant information in the uploaded documents to answer your question.",
                "sources": []
            }), 200

        # Generate answer using RAG
        print("Generating answer with RAG...")
        answer = generate_answer(question, retrieved_chunks)
        print(f"Generated answer: {answer[:100]}...")

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks[:3],  # Limit sources for readability
            "num_sources": len(retrieved_chunks)
        }), 200

    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/get-pdfs', methods=['GET'])
def get_pdfs():
    """Returns list of uploaded PDFs (without raw data)."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, size FROM pdf_files")
        rows = cursor.fetchall()
        conn.close()

        pdfs = [{"id": r[0], "filename": r[1], "size": r[2]} for r in rows]
        return jsonify(pdfs), 200

    except Exception as e:
        print(f"Error in get_pdfs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-chroma', methods=['GET'])
def test_chroma():
    """Test endpoint to check ChromaDB connection and content."""
    try:
        from services.chroma_service import collection
        
        # Get collection info
        collection_info = collection.get()
        
        return jsonify({
            "status": "success",
            "collection_name": "medical",
            "document_count": len(collection_info["documents"]) if collection_info["documents"] else 0,
            "sample_docs": collection_info["documents"][:2] if collection_info["documents"] else []
        }), 200
    
    except Exception as e:
        print(f"Error testing ChromaDB: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=5000)