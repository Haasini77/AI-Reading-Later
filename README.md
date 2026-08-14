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

The application sends the article content to the Flask backend, which communicates with the Groq API to generate a concise and meaningful summary.

The generated summary helps users quickly understand the main ideas without reading the entire article.

### AI Quiz Generation

The application can automatically generate multiple-choice quiz questions from article content.

The generated quiz helps users test their understanding of the topic and calculates their score after completing the quiz.

---

## 🔄 How It Works

1. User opens the AI Reading Later application.
2. User saves an article by entering its title and URL.
3. The article details are stored in the SQLite database.
4. User navigates to the AI Summary section.
5. User enters the article title and content.
6. The frontend sends the article data to the Flask backend.
7. The backend sends the content to the Groq API.
8. Groq AI generates a concise summary and important points.
9. User can use the article content to generate an AI quiz.
10. The AI generates multiple-choice questions.
11. The quiz evaluates the user's answers.
12. The application calculates and displays the user's score.
13. Progress and quiz performance can be viewed through the Progress section.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    │     Web Browser      │
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
                    │    Flask Backend     │
                    │       Python         │
                    └───────┬───────┬──────┘
                            │       │
                  ┌─────────┘       └──────────┐
                  ▼                            ▼
        ┌──────────────────┐          ┌──────────────────┐
        │      SQLite      │          │     Groq API     │
        │     Database     │          │     AI Model     │
        └──────────────────┘          └──────────────────┘
```

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask
- Flask-CORS

### Database

- SQLite

### AI

- Groq API
- Llama 3.3

### Development Tools

- Visual Studio Code
- Git
- GitHub

### Deployment

- Render

---

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
├── README.md
└── requirements.txt
```

---

## 📌 Main Sections

### 🏠 Home

Provides an introduction to the AI Reading Later application and its main features.

### ➕ Add Article

Allows users to save an article by entering:

- Article title
- Article URL

The article details are stored in the SQLite database.

### 🤖 AI Summary

Allows users to enter article content and generate an AI-powered summary using the Groq API.

The generated result includes:

- Summary
- Important points
- Key concepts
- Conclusion

### 🧠 AI Quiz

Generates multiple-choice questions based on article content and evaluates the user's answers.

### 📚 My Articles

Displays the articles saved by the user for later reading.

Users can also delete saved articles when they are no longer needed.

### 📊 Progress

Displays reading and quiz-related progress such as:

- Saved articles
- Quizzes taken
- Quiz scores
- Average performance

---

## 🔐 API Security

The Groq API key is stored securely as an environment variable on the deployment platform.

The API key is not included directly in the source code or frontend files.

Example:

```text
GROQ_API_KEY=your_groq_api_key
```

Never upload your actual API key to GitHub.

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Haasini77/AI-Reading-Later.git
```

### 2. Navigate to the Project

```bash
cd AI-Reading-Later
```

### 3. Install Dependencies

Install the Python dependencies listed in the project's `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API Key

Set the Groq API key as an environment variable.

```text
GROQ_API_KEY=your_groq_api_key
```

Do not share or commit your actual API key.

### 5. Run the Backend

```bash
python backend/app.py
```

### 6. Open the Application

Open the frontend in a browser or use the deployed application:

https://ai-reading-later-1.onrender.com

---

## ☁️ Deployment

The application is deployed using Render.

### Frontend

AI-Reading-Later-1

### Backend

AI-Reading-Later-Backend

The frontend communicates with the deployed Flask backend through HTTP requests.

---

## 🗄️ Database

The application uses SQLite to store saved article information.

The Flask backend automatically initializes the database when the application starts.

Database file:

```text
articles.db
```

---

## 🔌 Backend API

The Flask backend provides REST API endpoints for communication between the frontend, database, and AI service.

The backend handles:

- Saving articles
- Retrieving saved articles
- Deleting articles
- Generating AI summaries
- Generating AI quizzes
- Testing AI connectivity

---

## 🎯 Use Cases

AI Reading Later can be useful for:

- 📖 Students
- 🧑‍💻 Developers
- 🔬 Researchers
- 📰 Regular readers
- 🎓 Learners
- 📚 Anyone who wants to understand articles efficiently

---

## 🚀 Future Enhancements

Possible future improvements include:

- 🔐 User authentication and login
- ☁️ Cloud database integration
- 📄 Automatic article content extraction from URLs
- 🎙️ AI-generated audio summaries
- 🌍 Multi-language summaries
- 🔖 Article categories and tags
- 🔍 Search and filter functionality
- 📱 Progressive Web App support
- 📈 Advanced learning analytics
- 🏆 Gamification and achievement badges

---

## 💡 Project Highlights

This project demonstrates practical implementation of:

- Full-stack web development
- REST API communication
- Flask backend development
- SQLite database management
- Generative AI integration
- Groq API integration
- Environment variable management
- Frontend-backend integration
- Cloud deployment using Render
- Version control using Git and GitHub

---

## 👩‍💻 Author

### Haasini Obilisetty

B.Tech – Artificial Intelligence & Data Science

Interested in Artificial Intelligence, Data Science, Web Development, and building practical AI-powered applications.

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is created for educational and portfolio purposes.
