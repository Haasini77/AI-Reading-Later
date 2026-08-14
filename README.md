# 🤖 AI Reading Later

An AI-powered reading assistant that helps users save articles, generate AI summaries, and test their understanding through AI-generated quizzes.

## ✨ Features

- 📚 Save articles for later reading
- 🤖 Generate AI-powered article summaries
- 🧠 Generate quizzes from article content
- 📊 Track saved articles and quiz performance
- 💾 Store articles using SQLite database
- ⚡ Local AI processing using Ollama + Llama 3.2

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- SQLite

### AI
- Ollama
- Llama 3.2

### Development Tools
- Visual Studio Code
- Git
- GitHub

## 🔄 How It Works

1. User saves an article by entering its title and URL.
2. The article is stored in the SQLite database.
3. User can enter article content in the AI Summary section.
4. The backend sends the content to the local Ollama Llama 3.2 model.
5. AI generates a concise summary and important points.
6. User can generate a quiz based on article content.
7. The quiz evaluates the user's answers and calculates the score.
8. The dashboard displays saved articles, quizzes taken, and average score.

## 🧠 AI Integration

The project uses **Ollama with Llama 3.2** for local AI processing.

The Flask backend communicates with Ollama through its local API to generate article summaries and quizzes.

## 📁 Project Structure

```text
AI-Reading-Later/
│
├── index.html
├── style.css
├── script.js
│
├── backend/
│   └── app.py
│
├── .gitignore
└── README.md
