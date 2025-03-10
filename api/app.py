from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
    static_folder='../static',    # Update static folder path
    template_folder='../templates' # Update templates folder path
)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    level = data.get('level')
    topic = data.get('topic')
    api_key = data.get('apiKey')
    
    if not all([level, topic, api_key]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    prompt = f"""
    Create an English language quiz for {level} level English learners on the topic of "{topic}".
    
    The quiz should include:
    1. A title for the quiz
    2. A short reading passage (if appropriate for the topic)
    3. 5 multiple-choice questions
    
    For each question, provide:
    - The question text
    - 4 possible answers (A, B, C, D)
    - The correct answer
    - A brief explanation for the correct answer (optional)
    
    Format your response as a JSON object with the following structure:
    {{
      "title": "Quiz Title",
      "passage": "Reading passage text (if applicable, otherwise null)",
      "questions": [
        {{
          "text": "Question 1 text",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correctAnswer": "The correct option text",
          "explanation": "Explanation for the correct answer (optional)"
        }},
        // more questions...
      ]
    }}
    """
    
    try:
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-2.0:generateContent',
            headers={
                'Content-Type': 'application/json',
                'x-goog-api-key': api_key
            },
            json={
                'contents': [
                    {
                        'parts': [
                            {
                                'text': prompt
                            }
                        ]
                    }
                ],
                'generationConfig': {
                    'temperature': 0.7,
                    'topK': 40,
                    'topP': 0.95,
                    'maxOutputTokens': 2048,
                }
            }
        )
        
        if not response.ok:
            return jsonify({'error': 'Failed to generate quiz from Gemini API'}), response.status_code
        
        data = response.json()
        
        # Extract the JSON from the response
        text_content = data['candidates'][0]['content']['parts'][0]['text']
        
        # Find the JSON object in the text
        import re
        json_match = re.search(r'({[\s\S]*})', text_content)
        
        if not json_match:
            return jsonify({'error': 'Failed to parse quiz data from Gemini response'}), 500
        
        try:
            quiz_data = json.loads(json_match.group(1))
            return jsonify(quiz_data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Failed to parse quiz data from Gemini response'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)