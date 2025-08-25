from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)
CORS(app)

@app.route('/api/upload-pdf', methods=['POST'])  # Missing @ symbol!
def upload_pdf():
    try:
        file = request.files['pdf']          
        
        print(file.filename)        
        print(file.content_type)    
        
        file.seek(0, os.SEEK_END)
        file_size = file.tell()    
        file.seek(0)               
        
        file_path = os.path.join('uploads', 'some_name.pdf')
        file.save(file_path)
        
        return jsonify({
            'message': 'File saved successfully',
            'filename': file.filename,
            'size': file_size
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)