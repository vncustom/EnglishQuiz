# English Quiz Generator

A web application that automatically generates customized English language quizzes using generative AI. The application creates multiple-choice questions for grammar, reading comprehension, and vocabulary practice at various difficulty levels.

## Features

- **Three Skills Categories**: Generate quizzes for Grammar, Reading, and Vocabulary
- **Five Difficulty Levels**: Beginner, Pre-Intermediate, Intermediate, Upper-Intermediate, and Advanced
- **Topic Customization**: Enter your own topic or let the system choose an appropriate one
- **Automatic Quiz Generation**: Uses Gemini AI to create contextually appropriate questions
- **Scoring System**: Get immediate feedback on your answers with a detailed breakdown
- **Responsive Design**: Works on desktop and mobile devices

## Demo

Access the live application at [URL of your deployed app]

![App Screenshot](screenshot.png)

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Google's Gemini 2.0 Flash Lite model
- **Deployment**: Vercel

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Gemini API keys (requires setting up two keys for alternating usage)

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/english-quiz-generator.git
   cd english-quiz-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export GEMINI_KEY1=your_first_api_key
   export GEMINI_KEY2=your_second_api_key
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open `http://localhost:8000` in your browser

### Deploying to Vercel

1. Make sure you have the Vercel CLI installed:
   ```
   npm install -g vercel
   ```

2. Add your API keys to Vercel:
   ```
   vercel secrets add GEMINI_KEY1 your_first_api_key
   vercel secrets add GEMINI_KEY2 your_second_api_key
   ```

3. Deploy the application:
   ```
   vercel
   ```

## Usage

1. Select the skill you want to practice (Grammar, Reading, or Vocabulary)
2. Choose the difficulty level appropriate for you
3. Enter a topic (optional) or leave blank for a randomly selected topic
4. Click "Tạo Bài Tập Mới" to generate your quiz
5. Answer the multiple-choice questions
6. Submit your answers to see your score and review correct answers

## How It Works

The application:
1. Takes your skill, level, and topic preferences
2. Forms a detailed prompt in Vietnamese for the Gemini AI model
3. Processes the AI-generated content to extract questions, options, and answers
4. Displays the formatted quiz in an interactive interface
5. Scores your responses and provides feedback

## API Considerations

- The application alternates between two API keys to avoid hitting rate limits
- Each quiz generation uses one API call
- The system is optimized for Gemini 2.0 Flash Lite with Vietnamese prompting for better quality educational content

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google's Gemini AI for powering the quiz generation
- Vercel for hosting the application
