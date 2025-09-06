# MediLens

A simple AI assistant that helps you understand medical reports and symptoms. Upload your lab results or describe what you're experiencing, and get clear explanations in plain language.

## What it does

- Analyzes medical PDFs and explains key findings
- Answers questions about symptoms and health concerns
- Provides medical guidance with appropriate disclaimers
- Uses GPT-4 for accurate, professional responses

## Tech Stack

- **Frontend**: React with modern CSS
- **Backend**: Flask with SQLite for file storage
- **AI**: OpenAI GPT-4 API
- **PDF Processing**: PyPDF2 for text extraction

## Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/medilens.git
cd medilens
```

2. Install backend dependencies
```bash
pip install flask flask-cors openai PyPDF2 python-dotenv
```

3. Create a `.env` file with your OpenAI API key
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the backend
```bash
python routes.py
```

5. Start the React frontend
```bash
npm install
npm start
```

## Usage

1. Open the app in your browser
2. Upload a medical PDF or type your symptoms
3. Get AI-powered explanations and guidance
4. Always consult healthcare professionals for official medical advice

## Features

- PDF upload and analysis
- Real-time chat interface
- File storage in SQLite database
- Responsive design for mobile and desktop
- Medical disclaimers and safety warnings

## Important Note

This tool provides educational information only. Always consult qualified healthcare providers for medical diagnosis and treatment decisions.

## Contributing

Feel free to submit issues or pull requests. Keep the focus on making medical information more accessible while maintaining safety and accuracy.

## License

MIT License - see LICENSE file for details
