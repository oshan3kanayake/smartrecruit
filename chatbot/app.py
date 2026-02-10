from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
import re

app = Flask(__name__)

# HTML Template (embedded)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartRecruit - AI Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        ...
        /* Chatbot Styles */
        /* Scoring Styles */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 SmartRecruit AI</h1>
            <p>Your intelligent recruitment assistant</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('chat')">💬 Chatbot</button>
            <button class="tab" onclick="switchTab('score')">📊 AI Scoring</button>
        </div>
        
        <!-- Chatbot Tab -->
        <div id="chat" class="tab-content active">
            <div id="chatbox"></div>
            <div class="input-group">
                <input type="text" id="userInput" placeholder="Ask me anything about recruitment..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <!-- Scoring Tab -->
        <div id="score" class="tab-content">
            <div class="form-group">
                <label>📄 Job Description:</label>
                <textarea id="jobDesc" placeholder="Enter the job requirements and description..."></textarea>
            </div>
            <div class="form-group">
                <label>👤 Resume/CV:</label>
                <textarea id="resume" placeholder="Paste the candidate's resume here..."></textarea>
            </div>
            <button onclick="calculateScore()">Calculate Match Score</button>
            <div id="result"></div>
        </div>
    </div>
    <script>
        // JS to switch tabs, send chat, calculate score
    </script>
</body>
</html>
"""

# Simple chatbot responses
def get_bot_response(message):
    message = message.lower()
    
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! How can I help you with recruitment today?"
    elif any(word in message for word in ['job', 'position', 'vacancy', 'opening']):
        return "Looking for jobs? I can help! You can also use the AI Scoring tab to see how well a candidate matches a job description."
    ...
    else:
        return "I'm here to help with recruitment! Try asking about jobs, resumes, or use the AI Scoring feature to match candidates with positions."

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        bot_response = get_bot_response(user_message)
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': 'Sorry, I encountered an error.'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        job_desc = data.get('job_description', '')
        resume = data.get('resume', '')
        if not job_desc or not resume:
            return jsonify({'error': 'Missing data'}), 400
        # Call predict.py
        combined_input = f"{job_desc}|||SEPARATOR|||{resume}"
        result = subprocess.run(
            ['python3', 'predict.py', combined_input],
            capture_output=True,
            text=True,
            timeout=30
        )
        score = int(result.stdout.strip() or 0)
        return jsonify({'score': score})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
