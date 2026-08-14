from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import json

# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)

# ==========================================
# OLLAMA SETUP
# ==========================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

# ==========================================
# DATABASE
# ==========================================

DATABASE = "articles.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# CREATE DATABASE TABLE
# ==========================================

def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():
    return jsonify({
        "message": "AI Reading Later Backend is Running! 🚀",
        "ai": "Ollama + Llama 3.2"
    })


# ==========================================
# GET ALL ARTICLES
# ==========================================

@app.route("/api/articles", methods=["GET"])
def get_articles():

    connection = get_db_connection()

    articles = connection.execute(
        "SELECT * FROM articles ORDER BY id DESC"
    ).fetchall()

    connection.close()

    result = []

    for article in articles:
        result.append({
            "id": article["id"],
            "title": article["title"],
            "url": article["url"]
        })

    return jsonify(result)


# ==========================================
# SAVE ARTICLE
# ==========================================

@app.route("/api/articles", methods=["POST"])
def save_article():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    title = data.get("title")
    url = data.get("url")

    if not title or not url:
        return jsonify({
            "error": "Title and URL are required"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO articles (title, url)
        VALUES (?, ?)
        """,
        (title, url)
    )

    connection.commit()

    article_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Article saved successfully",
        "id": article_id,
        "title": title,
        "url": url
    }), 201


# ==========================================
# DELETE ARTICLE
# ==========================================

@app.route("/api/articles/<int:article_id>", methods=["DELETE"])
def delete_article(article_id):

    connection = get_db_connection()

    cursor = connection.execute(
        "DELETE FROM articles WHERE id = ?",
        (article_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:
        return jsonify({
            "error": "Article not found"
        }), 404

    return jsonify({
        "message": "Article deleted successfully"
    })


# ==========================================
# AI SUMMARY USING OLLAMA
# ==========================================

@app.route("/api/summarize", methods=["POST"])
def summarize_article():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    title = data.get("title", "")
    content = data.get("content", "")

    if not content:
        return jsonify({
            "error": "Article content is required"
        }), 400

    prompt = f"""
You are an AI reading assistant.

Summarize the following article clearly for a college student.

Give the response in this format:

SUMMARY:
Write a short and clear summary.

IMPORTANT POINTS:
- Point 1
- Point 2
- Point 3

KEY CONCEPTS:
- Concept 1
- Concept 2
- Concept 3

CONCLUSION:
Give a simple conclusion.

Use simple English and avoid unnecessary details.

Article Title:
{title}

Article Content:
{content}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        summary = result.get("response", "")

        return jsonify({
            "success": True,
            "summary": summary
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "success": False,
            "error": "Ollama is not running. Please start Ollama."
        }), 500

    except Exception as error:

        print("AI SUMMARY ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# TEST OLLAMA AI
# ==========================================

@app.route("/api/test-ai", methods=["GET"])
def test_ai():

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": "Say hello and confirm that the AI Reading Later project is connected to Ollama.",
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return jsonify({
            "success": True,
            "message": result.get("response", "")
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# AI QUIZ GENERATION
# ==========================================

@app.route("/api/quiz", methods=["POST"])
def generate_quiz():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    title = data.get("title", "")
    content = data.get("content", "")

    if not content:
        return jsonify({
            "error": "Article content is required"
        }), 400

    prompt = f"""
You are an AI quiz generator.

Create exactly 5 multiple-choice questions
from the article below.

Return ONLY valid JSON.

Use this exact format:

{{
    "quiz": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": 0
        }}
    ]
}}

Rules:
- Exactly 5 questions.
- Exactly 4 options for every question.
- "answer" must be 0, 1, 2, or 3.
- 0 means Option A.
- 1 means Option B.
- 2 means Option C.
- 3 means Option D.
- Questions must be based only on the article.
- Use simple English.
- Return only JSON.

Article Title:
{title}

Article Content:
{content}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        ai_response = result.get("response", "")

        quiz_data = json.loads(ai_response)

        quiz = quiz_data.get("quiz", [])

        if len(quiz) == 0:
            raise Exception("No quiz questions generated")

        return jsonify({
            "success": True,
            "quiz": quiz
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "success": False,
            "error": "Ollama is not running."
        }), 500

    except json.JSONDecodeError:

        return jsonify({
            "success": False,
            "error": "AI returned invalid quiz format. Please try again."
        }), 500

    except Exception as error:

        print("QUIZ ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        port=5000
    )