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
load_dotenv()

app = Flask(__name__)
CORS(app)

DB_NAME = "MediLens.db"

# --- Chroma Cloud client ---
client = chromadb.HttpClient(
    ssl=True,
    host="api.trychroma.com",
    tenant="c62ca6f6-ebde-4f3e-a727-885904e35df1",
    database="MediLens",
    headers={
        "x-chroma-token": "ck-DhNfVgeXRLgL42wfYfSzqBbBs89Mbzp3gE4SCKrwX3as"
    }
)

# Get your existing collection
collection = client.get_collection(name="medical")

# --- Use sentence-transformers for 384-dimension embeddings ---
# This model produces 384-dimension embeddings, which matches your ChromaDB collection
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

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
    """
    Split text into overlapping chunks.
    chunk_size: max characters per chunk
    overlap: repeated characters between chunks (for context)
    """
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
        if 'pdf' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['pdf']
        file_data = file.read()
        file_size = len(file_data)

        # --- Save PDF in SQLite ---
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pdf_files (filename, content_type, data, size)
            VALUES (?, ?, ?, ?)
        """, (file.filename, file.content_type, file_data, file_size))
        pdf_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # --- Extract text ---
        file.stream.seek(0)
        pdf_text = extract_text_from_pdf(file.stream)

        if pdf_text.strip():
            # --- 1. Chunk text ---
            chunks = chunk_text(pdf_text, chunk_size=1000, overlap=200)

            # --- 2. Embed + query Chroma with first few chunks ---
            query_results = []
            for i, chunk in enumerate(chunks[:5]):  # only first 5 chunks for now
                # Use sentence-transformers instead of OpenAI (produces 384-dim embeddings)
                embedding = embedding_model.encode(chunk).tolist()

                results = collection.query(
                    query_embeddings=[embedding],
                    n_results=2
                )

                query_results.append({
                    "chunk_index": i,
                    "chunk_preview": chunk[:150],  # preview for debugging
                    "results": results
                })

            print("ChromaDB Query Results:", query_results)

            return jsonify({
                "message": "File saved and queried with chunks",
                "filename": file.filename,
                "size": file_size,
                "chunks_queried": len(query_results),
                "query_results": query_results
            }), 200
        else:
            return jsonify({
                "message": "File saved, but no extractable text",
                "filename": file.filename,
                "size": file_size
            }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()  # print full error to console
        return jsonify({"error": str(e)}), 500


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
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-pdf/<int:pdf_id>', methods=['GET'])
def download_pdf(pdf_id):
    """Download a specific PDF by ID."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT filename, content_type, data FROM pdf_files WHERE id = ?", (pdf_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return jsonify({'error': 'File not found'}), 404

        filename, content_type, file_data = row

        return (file_data, 200, {
            "Content-Type": content_type,
            "Content-Disposition": f"attachment; filename={filename}"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)