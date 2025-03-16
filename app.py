from flask import Flask, render_template, request, jsonify
import os
import requests
import re
import random

app = Flask(__name__)
app.secret_key = "quiz_generator_secret_key"

# Counter to track API requests for alternating between keys
request_counter = 0

# Topic suggestions based on skill and level
TOPIC_SUGGESTIONS = {
    "grammar": {
        "beginner": ["Present Simple", "Present Continuous", "Articles", "Possessive Adjectives", "Prepositions of Place"],
        "pre-intermediate": ["Past Simple", "Past Continuous", "Comparatives", "Superlatives", "Going to Future"],
        "intermediate": ["Present Perfect", "Past Perfect", "Conditionals Type 1 & 2", "Passive Voice", "Reported Speech"],
        "upper-intermediate": ["Future Perfect", "Future Continuous", "Conditionals Type 3", "Wish Clauses", "Modal Verbs"],
        "advanced": ["Inversion", "Cleft Sentences", "Subjunctive", "Participle Clauses", "Advanced Conditionals"]
    },
    "reading": {
        "beginner": ["Family", "Daily Routines", "Food", "Hobbies", "Weather"],
        "pre-intermediate": ["Travel", "Health", "Education", "Technology", "Environment"],
        "intermediate": ["Culture", "Social Media", "Work Life", "Global Issues", "Science"],
        "upper-intermediate": ["Psychology", "Economics", "Politics", "Literature", "Innovation"],
        "advanced": ["Philosophy", "Ethics", "Globalization", "Climate Change", "Artificial Intelligence"]
    }
    "vocabulary": {
        "beginner": ["Basic Adjectives (Colors, Sizes)", "Numbers and Time", "Family Members", "Everyday Objects", "Common Verbs (eat, go, see)"],
        "pre-intermediate": ["Travel and Transportation", "Jobs and Occupations", "Feelings and Emotions", "Shopping and Money", "Food and Cooking"],
        "intermediate": ["Phrasal Verbs (take off, give up)", "Collocations (make a decision, do homework)", "Work and Business", "Health and Fitness", "Describing People (appearance, personality)"],
        "upper-intermediate": ["Idioms (hit the nail on the head)", "Academic Vocabulary (analyze, evaluate)", "Technology and Innovation", "Environment and Sustainability", "Relationships and Society"],
        "advanced": ["Advanced Idioms (burn the midnight oil)", "Synonyms and Antonyms (e.g., happy vs. elated)", "Legal and Political Terms", "Scientific Vocabulary", "Cultural Expressions and Proverbs"]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    global request_counter
    
    data = request.json
    skill = data.get('skill')
    level = data.get('level')
    topic = data.get('topic', '').strip()
    
    # If topic is empty or too short, select a random appropriate topic
    if not topic or len(topic) < 3:
        available_topics = TOPIC_SUGGESTIONS.get(skill, {}).get(level, [])
        if available_topics:
            topic = random.choice(available_topics)
        else:
            # Fallback topics if the skill/level combination is not found
            topic = "General English" if skill == "reading" else "Basic Grammar"
    
    # Alternate between keys
    key_to_use = "KEY1" if request_counter % 2 == 0 else "KEY2"
    request_counter += 1
    
    # Get the appropriate API key
    api_key = os.environ.get(f"GEMINI_{key_to_use}")
    
    if not api_key:
        return jsonify({"error": f"API key {key_to_use} is not configured"}), 500
    
    role_prompt = "Bạn là một giáo viên tiếng Anh có 15 năm kinh nghiệm giảng dạy và ra đề thi. Hãy tạo "
    content_prompt = ""
    
    if skill == 'grammar':
        content_prompt = f"{role_prompt}5 câu hỏi trắc nghiệm về ngữ pháp {topic} cho trình độ {level}.\n"
        content_prompt += "Yêu cầu:\n"
        content_prompt += "- Câu hỏi phải phản ánh đúng trình độ học viên\n"
        content_prompt += "- Lựa chọn đáp án gây nhiễu tốt\n"
        content_prompt += "- Định dạng:\n"
        content_prompt += "Câu 1: [Nội dung]\n"
        content_prompt += "A. [Option A]\n"
        content_prompt += "B. [Option B]\n"
        content_prompt += "C. [Option C]\n"
        content_prompt += "D. [Option D]\n"
        content_prompt += "Đáp án: [Chữ cái]"
    elif skill == 'reading':
        length_requirement = ""
        if level == 'beginner':
            length_requirement = "100-150 từ, từ vựng đơn giản"
        elif level == 'pre-intermediate':
            length_requirement = "150-250 từ, từ vựng A2, câu có cấu trúc đơn giản, một số liên từ cơ bản"
        elif level == 'intermediate':
            length_requirement = "250-350 từ, từ vựng B1, bao gồm một số cụm từ thông dụng và câu ghép"
        elif level == 'upper-intermediate':
            length_requirement = "350-500 từ, từ vựng B2, cấu trúc đa dạng, có yếu tố suy luận"
        else:
            length_requirement = "500-800 từ, từ vựng C1-C2, câu phức tạp, chủ đề trừu tượng hoặc học thuật"
        
        content_prompt = f"{role_prompt}một bài đọc hiểu về {topic} với các yêu cầu sau:\n"
        content_prompt += f"- Độ dài: {length_requirement}\n"
        content_prompt += "- Nội dung hấp dẫn, phù hợp trình độ\n"
        content_prompt += "- Sau đoạn văn tạo 5 câu hỏi trắc nghiệm\n"
        content_prompt += "- Định dạng:\n"
        content_prompt += "[Passage]\n\n"
        content_prompt += "Câu 1: [Nội dung]\n"
        content_prompt += "A. [Option A]\n"
        content_prompt += "B. [Option B]\n"
        content_prompt += "C. [Option C]\n"
        content_prompt += "D. [Option D]\n"
        content_prompt += "Đáp án: [Chữ cái]"
    else:
        length_requirement = ""
        if level == 'beginner':
            length_requirement = "Hoàn thành câu ngắn, từ vựng A1, ngữ cảnh quen thuộc"
        elif level == 'pre-intermediate':
            length_requirement = "Chọn từ/cụm từ trong câu 10-15 từ, từ vựng A2, ngữ cảnh đơn giản"
        elif level == 'intermediate':
            length_requirement = "Chọn từ trong đoạn 50-70 từ, từ vựng B1, có thành ngữ cơ bản"
        elif level == 'upper-intermediate':
            length_requirement = "Chọn từ/cụm từ trong đoạn 80-100 từ, từ vựng B2, ngữ cảnh phức tạp"
        else:
            length_requirement = "Chọn từ, cụm từ đồng nghĩa hoặc trái nghĩa trong đoạn 100-120 từ, từ vựng C1-C2, thành ngữ học thuật"
        
        content_prompt = f"{role_prompt} 5 câu hỏi trắc nghiệm về {topic} với các yêu cầu sau:\n"
        content_prompt += f"- Hình thức câu hỏi: {length_requirement}\n"
        content_prompt += "- Nội dung hấp dẫn, phù hợp trình độ\n"
        content_prompt += "- Định dạng:\n"
        content_prompt += "Câu 1: [Nội dung]\n"
        content_prompt += "A. [Option A]\n"
        content_prompt += "B. [Option B]\n"
        content_prompt += "C. [Option C]\n"
        content_prompt += "D. [Option D]\n"
        content_prompt += "Đáp án: [Chữ cái]"
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}",
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": content_prompt
                            }
                        ]
                    }
                ]
            }
        )
        
        response.raise_for_status()
        data = response.json()
        response_text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Parse the quiz data
        quiz_data = parse_quiz_response(response_text, skill)
        
        # Add the selected topic to the response
        return jsonify({
            "quiz": quiz_data,
            "keyUsed": key_to_use,
            "selectedTopic": topic
        })
    
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return jsonify({"error": "Failed to generate quiz"}), 500

def parse_quiz_response(text, skill):
    # Clean up the response text
    clean_text = re.sub(r'Tuyệt vời!.*?\n', '', text)
    clean_text = re.sub(r'Dưới đây là.*?\n', '', clean_text)
    clean_text = re.sub(r'\*\*.*?\*\*\n', '', clean_text)
    
    if skill == "reading":
        passage_end = clean_text.find("Câu 1:")
        passage = clean_text[:passage_end].strip() if passage_end != -1 else ""
        questions = parse_questions(clean_text[passage_end:] if passage_end != -1 else clean_text)
        return {
            "skill": skill,
            "passage": passage,
            "questions": questions
        }
    
    return {
        "skill": skill,
        "passage": None,
        "questions": parse_questions(clean_text)
    }

def parse_questions(text):
    questions = []
    question_blocks = re.split(r'Câu \d+:', text)[1:]
    
    for block in question_blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        question_text = lines[0]
        options = {}
        correct_answer = ""
        
        for line in lines[1:]:
            if re.match(r'^[A-D]\.', line):
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    key, value = parts
                    options[key[0]] = value.strip()
            elif line.startswith("Đáp án:"):
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    correct_answer = parts[1].strip()
        
        if question_text:
            questions.append({
                "question": question_text,
                "options": options,
                "correctAnswer": correct_answer
            })
    
    return questions

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)