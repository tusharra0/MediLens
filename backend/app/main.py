from flask import Flask
from routes import init_routes
import os

def create_app():
    app = Flask(__name__)
    
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
    
    os.makedirs('uploads', exist_ok=True)
    
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)