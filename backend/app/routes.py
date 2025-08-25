from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Only PDFs allowed'}), 400

    try:
        # Generate safe unique filename
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)

        # Save file
        file.save(filepath)
        file_size = os.path.getsize(filepath)

        # Extract text
        pdf_text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pdf_text += text
                if i < 3:  # print only first 3 pages for sanity
                    print(f"\n--- Page {i+1} ---\n{text}\n")

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'size': file_size,
            'preview': pdf_text[:500]  # return preview text
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
