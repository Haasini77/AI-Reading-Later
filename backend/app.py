from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import json
import os


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)


# ==========================================
# GROQ AI SETUP
# ==========================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_MODEL = "llama-3.3-70b-versatile"


# ==========================================
# DATABASE
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "articles.db")


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

    print("Database initialized successfully.")
    print("Database path:", DATABASE)


# IMPORTANT:
# Run database initialization when Flask
# application is imported by Gunicorn/Render.

init_db()


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "AI Reading Later Backend is Running! 🚀",
        "ai": "Groq + Llama 3.3"
    })


# ==========================================
# GET ALL ARTICLES
# ==========================================

@app.route("/api/articles", methods=["GET"])
def get_articles():

    try:

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

    except Exception as error:

        print("GET ARTICLES ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# SAVE ARTICLE
# ==========================================

@app.route("/api/articles", methods=["POST"])
def save_article():

    try:

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
            "success": True,
            "message": "Article saved successfully",
            "id": article_id,
            "title": title,
            "url": url
        }), 201

    except Exception as error:

        print("SAVE ARTICLE ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# DELETE ARTICLE
# ==========================================

@app.route("/api/articles/<int:article_id>", methods=["DELETE"])
def delete_article(article_id):

    try:

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
            "success": True,
            "message": "Article deleted successfully"
        })

    except Exception as error:

        print("DELETE ARTICLE ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# AI SUMMARY USING GROQ
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

    # Check API key
    if not GROQ_API_KEY:

        return jsonify({
            "success": False,
            "error": "GROQ_API_KEY is not configured on the server."
        }), 500


    # ==========================================
    # SUMMARY PROMPT
    # ==========================================

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

            GROQ_URL,

            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": GROQ_MODEL,

                "messages": [

                    {
                        "role": "system",
                        "content": "You are an AI reading assistant."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                "temperature": 0.3,

                "max_tokens": 1500
            },

            timeout=180
        )


        response.raise_for_status()

        result = response.json()

        summary = result["choices"][0]["message"]["content"]


        return jsonify({

            "success": True,

            "summary": summary

        })


    except requests.exceptions.ConnectionError:

        return jsonify({

            "success": False,

            "error": "Could not connect to Groq AI."

        }), 500


    except requests.exceptions.HTTPError as error:

        print("GROQ HTTP ERROR:", error)

        try:

            error_details = response.json()

        except Exception:

            error_details = str(error)

        return jsonify({

            "success": False,

            "error": f"Groq API error: {error_details}"

        }), 500


    except Exception as error:

        print("AI SUMMARY ERROR:", error)

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ==========================================
# TEST GROQ AI
# ==========================================

@app.route("/api/test-ai", methods=["GET"])
def test_ai():

    try:

        if not GROQ_API_KEY:

            return jsonify({

                "success": False,

                "error": "GROQ_API_KEY is not configured."

            }), 500


        response = requests.post(

            GROQ_URL,

            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": GROQ_MODEL,

                "messages": [

                    {
                        "role": "user",
                        "content": "Say hello and confirm that the AI Reading Later project is connected to Groq AI."
                    }

                ],

                "temperature": 0.2,

                "max_tokens": 100
            },

            timeout=60
        )


        response.raise_for_status()

        result = response.json()


        return jsonify({

            "success": True,

            "message": result["choices"][0]["message"]["content"]

        })


    except Exception as error:

        print("TEST AI ERROR:", error)

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ==========================================
# AI QUIZ GENERATION USING GROQ
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


    # Check API key
    if not GROQ_API_KEY:

        return jsonify({

            "success": False,

            "error": "GROQ_API_KEY is not configured on the server."

        }), 500


    # ==========================================
    # QUIZ PROMPT
    # ==========================================

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

            GROQ_URL,

            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": GROQ_MODEL,

                "messages": [

                    {
                        "role": "system",
                        "content": "You generate quizzes and return only valid JSON."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                "temperature": 0.2,

                "max_tokens": 2000,

                "response_format": {
                    "type": "json_object"
                }

            },

            timeout=180
        )


        response.raise_for_status()

        result = response.json()

        ai_response = result["choices"][0]["message"]["content"]


        # Convert AI response into Python dictionary
        quiz_data = json.loads(ai_response)

        quiz = quiz_data.get("quiz", [])


        if len(quiz) == 0:

            raise Exception("No quiz questions generated")


        # Validate quiz
        if len(quiz) != 5:

            raise Exception("AI did not generate exactly 5 questions")


        for question in quiz:

            if "question" not in question:

                raise Exception("Invalid question format")

            if "options" not in question:

                raise Exception("Options missing")

            if len(question["options"]) != 4:

                raise Exception("Each question must have exactly 4 options")

            if "answer" not in question:

                raise Exception("Answer missing")

            if question["answer"] not in [0, 1, 2, 3]:

                raise Exception("Invalid answer index")


        return jsonify({

            "success": True,

            "quiz": quiz

        })


    except requests.exceptions.ConnectionError:

        return jsonify({

            "success": False,

            "error": "Could not connect to Groq AI."

        }), 500


    except requests.exceptions.HTTPError as error:

        print("GROQ QUIZ HTTP ERROR:", error)

        try:

            error_details = response.json()

        except Exception:

            error_details = str(error)

        return jsonify({

            "success": False,

            "error": f"Groq API error: {error_details}"

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

    app.run(

        host="0.0.0.0",

        port=int(os.environ.get("PORT", 5000)),

        debug=False

    )