from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2
import sqlite3
from openai import OpenAI
import logging
import traceback
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_NAME = "MediLens.db"

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content_type TEXT NOT NULL,
            data BLOB NOT NULL,
            size INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create a table for storing chat sessions (optional, for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            pdf_id INTEGER,
            user_message TEXT,
            ai_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pdf_id) REFERENCES pdf_files (id)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def allowed_file(filename):
    """Check if the uploaded file is a PDF"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def store_pdf_in_db(file_data, filename, content_type):
    """Store PDF file in SQLite database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pdf_files (filename, content_type, data, size)
            VALUES (?, ?, ?, ?)
        """, (filename, content_type, file_data, len(file_data)))
        
        pdf_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"PDF stored in database with ID: {pdf_id}")
        return pdf_id
        
    except Exception as e:
        logger.error(f"Error storing PDF in database: {str(e)}")
        raise Exception(f"Failed to store PDF: {str(e)}")

def retrieve_pdf_from_db(pdf_id):
    """Retrieve PDF file from SQLite database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT filename, content_type, data, size
            FROM pdf_files WHERE id = ?
        """, (pdf_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'filename': result[0],
                'content_type': result[1],
                'data': result[2],
                'size': result[3]
            }
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving PDF from database: {str(e)}")
        return None

def extract_text_from_pdf_data(pdf_data):
    """Extract text content from PDF binary data"""
    try:
        text_content = ""
        
        # Create a BytesIO object from the binary data
        pdf_stream = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        
        # Extract text from all pages
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page_text
            except Exception as e:
                logger.warning(f"Could not extract text from page {page_num + 1}: {str(e)}")
                continue
        
        return text_content.strip()
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF data: {str(e)}")
        raise Exception(f"Failed to process PDF: {str(e)}")

def create_medical_prompt(user_message, pdf_content=None, filename=None):
    """Create a comprehensive medical expert prompt"""
    
    base_prompt = """You are Dr. MediLens, a highly experienced medical AI assistant with expertise across multiple medical specialties including internal medicine, diagnostics, pathology, radiology, and clinical research. You have access to the latest medical literature and guidelines.

Your role is to:
1. Analyze medical reports, symptoms, and health-related queries with clinical precision
2. Provide evidence-based medical insights and explanations
3. Suggest potential differential diagnoses when appropriate
4. Recommend appropriate next steps or follow-up care
5. Explain medical terminology in accessible language
6. Identify critical findings that require immediate medical attention

IMPORTANT DISCLAIMERS:
- You are an AI assistant providing educational information, not replacing professional medical advice
- Always recommend consulting with healthcare providers for diagnosis and treatment
- For emergency symptoms, advise immediate medical attention
- Maintain patient confidentiality and handle all information sensitively

RESPONSE FORMAT:
- Use clear, professional medical language
- Provide structured analysis when reviewing reports
- Include relevant medical context and explanations
- Highlight any concerning findings prominently
- End with appropriate recommendations for next steps"""

    if pdf_content and user_message:
        file_info = f" (from uploaded file: {filename})" if filename else ""
        prompt = f"""{base_prompt}

USER QUERY: {user_message}

MEDICAL DOCUMENT/REPORT CONTENT{file_info}:
{pdf_content}

Please provide a comprehensive medical analysis of the uploaded document in relation to the user's query. Focus on:
1. Key findings and their clinical significance
2. Any abnormal values or concerning results
3. Correlation with the user's symptoms or concerns
4. Recommended follow-up actions
5. Patient-friendly explanation of medical terms

Provide your expert medical assessment:"""

    elif pdf_content and not user_message:
        file_info = f" (from uploaded file: {filename})" if filename else ""
        prompt = f"""{base_prompt}

The user has uploaded a medical document without a specific question. Please provide a comprehensive review of this medical report.

MEDICAL DOCUMENT/REPORT CONTENT{file_info}:
{pdf_content}

Please analyze this medical document and provide:
1. Summary of key findings
2. Clinical significance of results
3. Any abnormal or noteworthy values
4. Recommended follow-up or next steps
5. Patient-friendly explanation of the report

Provide your expert medical assessment:"""

    elif user_message and not pdf_content:
        prompt = f"""{base_prompt}

USER QUERY/SYMPTOMS: {user_message}

The user is describing symptoms or asking a medical question without providing additional documentation. Please provide:
1. Analysis of the described symptoms
2. Possible differential diagnoses (if symptoms described)
3. Recommended diagnostic steps or tests
4. When to seek immediate medical care
5. General health guidance related to their concern

Provide your expert medical assessment:"""

    else:
        prompt = f"""{base_prompt}

The user has initiated a consultation but hasn't provided specific information yet. Please provide a helpful introduction explaining how you can assist with medical queries, symptom analysis, and report interpretation.

Provide a welcoming and informative response:"""

    return prompt

def get_gpt_response(prompt):
    """Get response from OpenAI GPT"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Use GPT-4 Turbo for better medical analysis
            messages=[
                {
                    "role": "system", 
                    "content": "You are a medical AI assistant with deep expertise in clinical medicine, diagnostics, and patient care."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.1,  # Low temperature for more consistent medical responses
            top_p=0.9
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise Exception(f"Failed to get AI response: {str(e)}")

def store_chat_session(session_id, pdf_id, user_message, ai_response):
    """Store chat session in database for future reference"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_sessions (session_id, pdf_id, user_message, ai_response)
            VALUES (?, ?, ?, ?)
        """, (session_id, pdf_id, user_message, ai_response))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Chat session stored with ID: {session_id}")
        
    except Exception as e:
        logger.error(f"Error storing chat session: {str(e)}")

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and message processing"""
    try:
        # Get user message
        user_message = request.form.get('message', '').strip()
        
        # Check if PDF file is uploaded
        pdf_file = request.files.get('pdf')
        pdf_content = None
        pdf_id = None
        filename = None
        
        if pdf_file and allowed_file(pdf_file.filename):
            # Secure the filename
            filename = secure_filename(pdf_file.filename)
            
            # Read file data
            file_data = pdf_file.read()
            content_type = pdf_file.content_type or 'application/pdf'
            
            logger.info(f"Processing PDF: {filename}, Size: {len(file_data)} bytes")
            
            # Store PDF in database
            pdf_id = store_pdf_in_db(file_data, filename, content_type)
            
            # Extract text from PDF
            pdf_content = extract_text_from_pdf_data(file_data)
            logger.info(f"Successfully extracted text from PDF: {len(pdf_content)} characters")
        
        # Validate that we have either message or PDF content
        if not user_message and not pdf_content:
            return jsonify({
                'success': False, 
                'error': 'Please provide either a message or upload a PDF file'
            }), 400
        
        # Create medical expert prompt
        medical_prompt = create_medical_prompt(user_message, pdf_content, filename)
        
        # Get AI response
        ai_response = get_gpt_response(medical_prompt)
        
        # Generate session ID and store chat session
        session_id = str(uuid.uuid4())
        store_chat_session(session_id, pdf_id, user_message, ai_response)
        
        # Prepare response
        response_data = {
            'success': True,
            'message': 'Analysis completed successfully',
            'ai_response': ai_response,
            'has_pdf': pdf_content is not None,
            'user_message': user_message,
            'pdf_processed': bool(pdf_content),
            'session_id': session_id,
            'pdf_id': pdf_id,
            'filename': filename
        }
        
        logger.info("Medical analysis completed successfully")
        return jsonify(response_data), 200
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_only():
    """Handle text-only medical queries"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Create medical prompt for text-only query
        medical_prompt = create_medical_prompt(user_message)
        
        # Get AI response
        ai_response = get_gpt_response(medical_prompt)
        
        # Generate session ID and store chat session
        session_id = str(uuid.uuid4())
        store_chat_session(session_id, None, user_message, ai_response)
        
        response_data = {
            'success': True,
            'message': 'Analysis completed successfully',
            'ai_response': ai_response,
            'has_pdf': False,
            'user_message': user_message,
            'session_id': session_id
        }
        
        logger.info("Text-only medical query processed successfully")
        return jsonify(response_data), 200
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/api/pdf/<int:pdf_id>', methods=['GET'])
def get_pdf(pdf_id):
    """Retrieve PDF file from database"""
    try:
        pdf_data = retrieve_pdf_from_db(pdf_id)
        
        if not pdf_data:
            return jsonify({
                'success': False,
                'error': 'PDF not found'
            }), 404
        
        return jsonify({
            'success': True,
            'filename': pdf_data['filename'],
            'size': pdf_data['size'],
            'content_type': pdf_data['content_type']
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving PDF: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all chat sessions (for admin/debug purposes)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cs.id, cs.session_id, cs.user_message, cs.created_at, 
                   pf.filename, pf.size
            FROM chat_sessions cs
            LEFT JOIN pdf_files pf ON cs.pdf_id = pf.id
            ORDER BY cs.created_at DESC
            LIMIT 50
        """)
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row[0],
                'session_id': row[1],
                'user_message': row[2][:100] + '...' if len(row[2]) > 100 else row[2],
                'created_at': row[3],
                'filename': row[4],
                'file_size': row[5]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'sessions': sessions
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving sessions: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MediLens API',
        'version': '1.0.0',
        'database': 'connected'
    }), 200

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle not found error"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY environment variable not set!")
        print("Error: Please set your OPENAI_API_KEY in your .env file")
        exit(1)
    
    print("MediLens API Server Starting...")
    print(f"Database: {DB_NAME}")
    print("SQLite3 storage enabled for PDF files")
    
    app.run(debug=True, host='0.0.0.0', port=5000)