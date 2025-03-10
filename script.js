document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const apiKeySection = document.getElementById('api-key-section');
    const quizFormSection = document.getElementById('quiz-form-section');
    const quizDisplaySection = document.getElementById('quiz-display-section');
    const resultsSection = document.getElementById('results-section');
    
    const apiKeyInput = document.getElementById('api-key');
    const submitApiKeyBtn = document.getElementById('submit-api-key');
    
    const levelSelect = document.getElementById('level');
    const topicInput = document.getElementById('topic');
    const generateQuizBtn = document.getElementById('generate-quiz');
    const loadingElement = document.getElementById('loading');
    
    const quizTitle = document.getElementById('quiz-title');
    const passageContainer = document.getElementById('passage-container');
    const passageText = document.getElementById('passage-text');
    const questionsContainer = document.getElementById('questions-container');
    const submitQuizBtn = document.getElementById('submit-quiz');
    
    const scoreElement = document.getElementById('score');
    const totalElement = document.getElementById('total');
    const percentageElement = document.getElementById('percentage');
    const scoreMessage = document.getElementById('score-message');
    const reviewContainer = document.getElementById('review-container');
    const newQuizBtn = document.getElementById('new-quiz');
    
    // State
    let apiKey = localStorage.getItem('geminiApiKey') || '';
    let currentQuiz = null;
    let userAnswers = [];
    
    // Initialize
    if (apiKey) {
        apiKeyInput.value = apiKey;
        showSection(quizFormSection);
    } else {
        showSection(apiKeySection);
    }
    
    // Event listeners
    submitApiKeyBtn.addEventListener('click', handleApiKeySubmit);
    generateQuizBtn.addEventListener('click', handleGenerateQuiz);
    submitQuizBtn.addEventListener('click', handleSubmitQuiz);
    newQuizBtn.addEventListener('click', handleNewQuiz);
    
    // Functions
    function handleApiKeySubmit() {
        const key = apiKeyInput.value.trim();
        if (!key) {
            alert('Please enter a valid API key');
            return;
        }
        
        apiKey = key;
        localStorage.setItem('geminiApiKey', apiKey);
        showSection(quizFormSection);
    }
    
    async function handleGenerateQuiz() {
        const level = levelSelect.value;
        const topic = topicInput.value.trim();
        
        if (!topic) {
            alert('Please enter a quiz topic');
            return;
        }
        
        showLoading(true);
        
        try {
            const response = await fetch('/generate-quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    level,
                    topic,
                    apiKey
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate quiz');
            }
            
            currentQuiz = await response.json();
            userAnswers = new Array(currentQuiz.questions.length).fill('');
            
            displayQuiz(currentQuiz);
            showSection(quizDisplaySection);
        } catch (error) {
            alert(error.message || 'An error occurred while generating the quiz');
        } finally {
            showLoading(false);
        }
    }
    
    function displayQuiz(quiz) {
        quizTitle.textContent = quiz.title;
        
        // Display passage if available
        if (quiz.passage && quiz.passage !== 'null') {
            passageText.textContent = quiz.passage;
            passageContainer.classList.remove('hidden');
        } else {
            passageContainer.classList.add('hidden');
        }
        
        // Display questions
        questionsContainer.innerHTML = '';
        quiz.questions.forEach((question, qIndex) => {
            const questionElement = document.createElement('div');
            questionElement.className = 'question';
            
            const questionText = document.createElement('p');
            questionText.textContent = `${qIndex + 1}. ${question.text}`;
            questionText.className = 'question-text';
            
            const optionsContainer = document.createElement('div');
            optionsContainer.className = 'options';
            
            question.options.forEach((option, oIndex) => {
                const optionElement = document.createElement('div');
                optionElement.className = 'option';
                
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = `question-${qIndex}`;
                radio.id = `q${qIndex}-o${oIndex}`;
                radio.value = option;
                radio.addEventListener('change', () => {
                    userAnswers[qIndex] = option;
                });
                
                const label = document.createElement('label');
                label.htmlFor = `q${qIndex}-o${oIndex}`;
                label.textContent = option;
                
                optionElement.appendChild(radio);
                optionElement.appendChild(label);
                optionsContainer.appendChild(optionElement);
            });
            
            questionElement.appendChild(questionText);
            questionElement.appendChild(optionsContainer);
            questionsContainer.appendChild(questionElement);
        });
    }
    
    function handleSubmitQuiz() {
        if (userAnswers.some(answer => answer === '')) {
            alert('Please answer all questions before submitting.');
            return;
        }
        
        const correctAnswers = currentQuiz.questions.map(q => q.correctAnswer);
        const score = userAnswers.reduce((acc, answer, index) => {
            return answer === correctAnswers[index] ? acc + 1 : acc;
        }, 0);
        
        const total = currentQuiz.questions.length;
        const percentage = Math.round((score / total) * 100);
        
        // Display results
        scoreElement.textContent = score;
        totalElement.textContent = total;
        percentageElement.textContent = percentage;
        
        if (percentage >= 80) {
            scoreMessage.textContent = 'Excellent work!';
        } else if (percentage >= 60) {
            scoreMessage.textContent = 'Good job!';
        } else {
            scoreMessage.textContent = 'Keep practicing!';
        }
        
        // Display review
        reviewContainer.innerHTML = '';
        currentQuiz.questions.forEach((question, qIndex) => {
            const isCorrect = userAnswers[qIndex] === question.correctAnswer;
            
            const reviewElement = document.createElement('div');
            reviewElement.className = 'review-question';
            
            const questionText = document.createElement('p');
            questionText.textContent = `${qIndex + 1}. ${question.text}`;
            questionText.className = 'question-text';
            
            reviewElement.appendChild(questionText);
            
            question.options.forEach(option => {
                const optionElement = document.createElement('div');
                const isUserAnswer = userAnswers[qIndex] === option;
                const isCorrectAnswer = question.correctAnswer === option;
                
                if (isUserAnswer && isCorrectAnswer) {
                    optionElement.className = 'review-option correct';
                    optionElement.textContent = `✓ ${option}`;
                } else if (isUserAnswer && !isCorrectAnswer) {
                    optionElement.className = 'review-option incorrect';
                    optionElement.textContent = `✗ ${option}`;
                } else if (isCorrectAnswer) {
                    optionElement.className = 'review-option correct';
                    optionElement.textContent = `${option} (Correct answer)`;
                } else {
                    optionElement.className = 'review-option';
                    optionElement.textContent = option;
                }
                
                reviewElement.appendChild(optionElement);
            });
            
            if (!isCorrect && question.explanation) {
                const explanationElement = document.createElement('div');
                explanationElement.className = 'explanation';
                explanationElement.textContent = `Explanation: ${question.explanation}`;
                reviewElement.appendChild(explanationElement);
            }
            
            reviewContainer.appendChild(reviewElement);
        });
        
        showSection(resultsSection);
    }
    
    function handleNewQuiz() {
        currentQuiz = null;
        userAnswers = [];
        showSection(quizFormSection);
    }
    
    function showSection(section) {
        apiKeySection.classList.add('hidden');
        quizFormSection.classList.add('hidden');
        quizDisplaySection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        
        section.classList.remove('hidden');
    }
    
    function showLoading(isLoading) {
        if (isLoading) {
            generateQuizBtn.classList.add('hidden');
            loadingElement.classList.remove('hidden');
        } else {
            generateQuizBtn.classList.remove('hidden');
            loadingElement.classList.add('hidden');
        }
    }
});