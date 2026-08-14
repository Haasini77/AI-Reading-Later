# 🤖 AI Reading Later

An AI-powered reading assistant that helps users save articles, generate AI-powered summaries, and test their understanding through automatically generated quizzes.

## 🌐 Live Demo

https://ai-reading-later-1.onrender.com

## 📂 GitHub Repository

https://github.com/Haasini77/AI-Reading-Later

---

## ✨ Features

- 📚 Save articles for later reading
- 🔗 Store article title and URL
- 🤖 Generate AI-powered article summaries
- 📝 Extract important points from article content
- 🧠 Generate AI-powered quizzes
- 🎯 Evaluate quiz answers automatically
- 📊 Track quiz performance and scores
- 📈 View reading and quiz progress
- 💾 Store saved articles using SQLite
- ⚡ Fast AI processing using Groq API
- 🌙 Modern dark-themed user interface
- 📱 Responsive web interface

---

## 🧠 AI Features

### AI Article Summarization

Users can enter article content and generate an AI-powered summary.

The application sends the article content to the backend, which communicates with the Groq API to generate a concise and meaningful summary.

The generated summary helps users quickly understand the main ideas without reading the entire article.

### AI Quiz Generation

The application can automatically generate quiz questions from article content.

The generated quiz helps users test their understanding of the topic and calculates their score after completing the quiz.

---

## 🔄 How It Works

1. User opens the AI Reading Later application.
2. User saves an article by entering its title and URL.
3. The article details are stored in the SQLite database.
4. User navigates to the AI Summary section.
5. User enters the article title and content.
6. The backend sends the content to the Groq API.
7. Groq AI generates a concise summary and important points.
8. User can use the same article content to generate an AI quiz.
9. The quiz evaluates the user's answers.
10. The application calculates and displays the user's score.
11. Progress and quiz performance can be viewed through the Progress section.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │   Web Browser        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   HTML / CSS / JS    │
                    └──────────┬───────────┘
                               │
                         HTTP Requests
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Flask          │
                    │      Backend         │
                    └───────┬───────┬──────┘
                            │       │
                  ┌─────────┘       └──────────┐
                  ▼                            ▼
        ┌──────────────────┐          ┌──────────────────┐
        │      SQLite      │          │     Groq API     │
        │     Database     │          │     AI Model     │
        └──────────────────┘          └──────────────────┘
