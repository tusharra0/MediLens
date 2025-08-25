from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2

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

@app.route('/api/upload-pdf', methods=['POST'])  
def upload_pdf():
    try:
        file = request.files['pdf'] 

        file_data = file.read()
        file_size = len(file_data)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pdf_files (filename, content_type, data, size)
            VALUES (?, ?, ?, ?)
        """, (file.filename, file.content_type, file_data, file_size))
        conn.commit()
        conn.close()

        return jsonify({
            'message': 'File saved successfully in database',
            'filename': file.filename,
            'size': file_size
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
