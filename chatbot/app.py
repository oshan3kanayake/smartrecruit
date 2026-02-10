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
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
        }
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            background: #f8f9fa;
            border: none;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s;
        }
        .tab:hover { background: #e9ecef; }
        .tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .tab-content {
            display: none;
            padding: 30px;
        }
        .tab-content.active { display: block; }
        
        /* Chatbot Styles */
        #chatbox {
            height: 400px;
            overflow-y: auto;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background: white;
            border: 2px solid #e0e0e0;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input[type="text"], textarea {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
        }
        button {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
        }
        button:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Scoring Styles */
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        textarea {
            width: 100%;
            min-height: 120px;
            resize: vertical;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            display: none;
        }
        .score-display {
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
        }
        .excellent { background: #d4edda; color: #155724; }
        .good { background: #cce5ff; color: #004085; }
        .average { background: #fff3cd; color: #856404; }
        .poor { background: #f8d7da; color: #721c24; }
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
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tab).classList.add('active');
        }

        // Chatbot
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(r => r.json())
            .then(data => {
                addMessage(data.response, 'bot');
            })
            .catch(() => {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            });
        }

        function addMessage(text, sender) {
            const chatbox = document.getElementById('chatbox');
            const msg = document.createElement('div');
            msg.className = `message ${sender}-message`;
            msg.textContent = text;
            chatbox.appendChild(msg);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        // AI Scoring
        function calculateScore() {
            const jobDesc = document.getElementById('jobDesc').value.trim();
            const resume = document.getElementById('resume').value.trim();
            const result = document.getElementById('result');

            if (!jobDesc || !resume) {
                result.innerHTML = '<p style="color: red;">Please fill in both fields!</p>';
                result.style.display = 'block';
                return;
            }

            result.innerHTML = '<p>⏳ Calculating score...</p>';
            result.style.display = 'block';

            fetch('/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({job_description: jobDesc, resume: resume})
            })
            .then(r => r.json())
            .then(data => {
                const score = data.score;
                let category = 'poor';
                let message = 'Not a good match';
                
                if (score >= 80) { category = 'excellent'; message = 'Excellent Match! 🎉'; }
                else if (score >= 60) { category = 'good'; message = 'Good Match! 👍'; }
                else if (score >= 40) { category = 'average'; message = 'Average Match 📊'; }
                
                result.className = category;
                result.innerHTML = `
                    <div class="score-display">${score}%</div>
                    <h3>${message}</h3>
                    <p>Match score based on AI analysis</p>
                `;
                result.style.display = 'block';
            })
            .catch(() => {
                result.innerHTML = '<p style="color: red;">Error calculating score. Please try again.</p>';
            });
        }

        // Welcome message
        window.onload = () => {
            addMessage("Hi! I'm SmartRecruit AI. Ask me about jobs, recruitment, or use the Scoring tab to match candidates!", 'bot');
        };
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
    
    elif any(word in message for word in ['resume', 'cv', 'application']):
        return "I can analyze resumes! Go to the 'AI Scoring' tab to compare a resume with a job description and get a match score."
    
    elif any(word in message for word in ['score', 'match', 'rating']):
        return "To get an AI match score, switch to the 'AI Scoring' tab and paste both the job description and candidate resume. I'll analyze the compatibility!"
    
    elif any(word in message for word in ['salary', 'pay', 'wage']):
        return "Salaries vary by role and location. Please check specific job listings for salary information."
    
    elif any(word in message for word in ['help', 'what can you do', 'features']):
        return "I can help with recruitment queries and provide AI-powered resume scoring. Use the 'AI Scoring' tab to match candidates with job descriptions!"
    
    elif any(word in message for word in ['thank', 'thanks']):
        return "You're welcome! Let me know if you need anything else."
    
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
