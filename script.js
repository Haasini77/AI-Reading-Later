// ==========================================
// ELEMENTS
// ==========================================

const saveArticleBtn =
    document.getElementById("saveArticleBtn");

const articlesContainer =
    document.getElementById("articlesContainer");

const articlesCount =
    document.getElementById("articlesCount");


// AI SUMMARY

const summarizeBtn =
    document.getElementById("summarizeBtn");

const summaryTitle =
    document.getElementById("summaryTitle");

const articleContent =
    document.getElementById("articleContent");

const summaryResult =
    document.getElementById("summaryResult");


// AI QUIZ

const generateQuizBtn =
    document.getElementById("generateQuizBtn");

const quizTitle =
    document.getElementById("quizTitle");

const quizContent =
    document.getElementById("quizContent");

const quizResult =
    document.getElementById("quizResult");

const quizzesCount =
    document.getElementById("quizzesCount");

const averageScore =
    document.getElementById("averageScore");


// QUIZ VARIABLES

let currentQuiz = [];

let currentQuestion = 0;

let quizScore = 0;

let quizCompleted = false;


// ==========================================
// LOAD ARTICLES
// ==========================================

async function loadArticles() {

    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/api/articles"
            );


        if (!response.ok) {

            throw new Error(
                "Could not load articles"
            );

        }


        const articles =
            await response.json();


        displayArticles(articles);

        updateDashboard(articles);

    }

    catch (error) {

        console.error(error);

        articlesContainer.innerHTML =

            `
            <p class="empty-message">

                ❌ Could not connect to backend.

            </p>
            `;

    }

}


// ==========================================
// DISPLAY ARTICLES
// ==========================================

function displayArticles(articles) {

    articlesContainer.innerHTML = "";


    if (articles.length === 0) {

        articlesContainer.innerHTML =

            `
            <p class="empty-message">

                📚 No articles saved yet.

            </p>
            `;

        return;

    }


    articles.forEach(
        function(article) {


            const articleCard =
                document.createElement("div");


            articleCard.className =
                "article-card";


            articleCard.innerHTML =

                `

                <div class="article-info">

                    <h3>
                        📖 ${escapeHTML(article.title)}
                    </h3>

                    <a
                        href="${article.url}"
                        target="_blank">

                        ${escapeHTML(article.url)}

                    </a>

                </div>


                <button
                    class="delete-btn"
                    onclick="deleteArticle(${article.id})">

                    🗑️ Delete

                </button>

                `;


            articlesContainer.appendChild(
                articleCard
            );

        }
    );

}


// ==========================================
// UPDATE DASHBOARD
// ==========================================

function updateDashboard(articles) {

    articlesCount.textContent =
        articles.length;

}


// ==========================================
// SAVE ARTICLE
// ==========================================

saveArticleBtn.addEventListener(
    "click",
    async function() {


        const title =
            document
                .getElementById("articleTitle")
                .value
                .trim();


        const url =
            document
                .getElementById("articleUrl")
                .value
                .trim();


        if (
            title === "" ||
            url === ""
        ) {

            alert(
                "Please enter both title and URL."
            );

            return;

        }


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/api/articles",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                title: title,

                                url: url

                            })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Failed to save article"
                );

            }


            document
                .getElementById("articleTitle")
                .value = "";


            document
                .getElementById("articleUrl")
                .value = "";


            alert(
                "Article saved successfully! 📚"
            );


            loadArticles();

        }


        catch (error) {

            console.error(error);

            alert(
                "Could not save article. ❌"
            );

        }

    }
);


// ==========================================
// DELETE ARTICLE
// ==========================================

async function deleteArticle(id) {

    const confirmDelete =
        confirm(
            "Are you sure you want to delete this article?"
        );


    if (!confirmDelete) {

        return;

    }


    try {

        const response =
            await fetch(
                `http://127.0.0.1:5000/api/articles/${id}`,
                {

                    method: "DELETE"

                }
            );


        if (!response.ok) {

            throw new Error(
                "Delete failed"
            );

        }


        alert(
            "Article deleted successfully! 🗑️"
        );


        loadArticles();

    }


    catch (error) {

        console.error(error);

        alert(
            "Could not delete article."
        );

    }

}


// ==========================================
// AI SUMMARY
// ==========================================

summarizeBtn.addEventListener(
    "click",
    async function() {


        const title =
            summaryTitle.value.trim();


        const content =
            articleContent.value.trim();


        if (
            title === "" ||
            content === ""
        ) {

            alert(
                "Please enter article title and content."
            );

            return;

        }


        summarizeBtn.disabled = true;

        summarizeBtn.textContent =
            "🤖 AI is reading...";


        summaryResult.innerHTML =

            `
            <div class="loading">

                <div class="spinner"></div>

                <p>
                    Llama 3.2 is analyzing your article...
                </p>

            </div>
            `;


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/api/summarize",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                title: title,

                                content: content

                            })

                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.error ||
                    "AI summarization failed"
                );

            }


            summaryResult.innerHTML =

                `
                <div class="success-label">

                    ✅ AI Summary Generated

                </div>

                <div class="summary-content">

                    ${formatSummary(
                        data.summary
                    )}

                </div>
                `;

        }


        catch (error) {

            console.error(error);


            summaryResult.innerHTML =

                `
                <div class="error-box">

                    ❌
                    <strong>
                        Could not generate summary
                    </strong>

                    <p>
                        ${escapeHTML(
                            error.message
                        )}
                    </p>

                </div>
                `;

        }


        finally {

            summarizeBtn.disabled =
                false;

            summarizeBtn.textContent =
                "✨ Summarize with AI";

        }

    }
);


// ==========================================
// AI QUIZ GENERATION
// ==========================================

generateQuizBtn.addEventListener(
    "click",
    async function() {


        const title =
            quizTitle.value.trim();


        const content =
            quizContent.value.trim();


        if (
            title === "" ||
            content === ""
        ) {

            alert(
                "Please enter article title and content."
            );

            return;

        }


        generateQuizBtn.disabled = true;

        generateQuizBtn.textContent =
            "🤖 Generating Quiz...";


        quizResult.innerHTML =

            `
            <div class="loading">

                <div class="spinner"></div>

                <p>
                    AI is creating your quiz...
                </p>

            </div>
            `;


        try {


            const response =
                await fetch(
                    "http://127.0.0.1:5000/api/quiz",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                title: title,

                                content: content

                            })

                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.error ||
                    "Quiz generation failed"
                );

            }


            currentQuiz =
                data.quiz;


            currentQuestion = 0;

            quizScore = 0;

            quizCompleted = false;


            displayQuizQuestion();


        }


        catch (error) {

            console.error(error);


            quizResult.innerHTML =

                `
                <div class="error-box">

                    ❌
                    <strong>
                        Could not generate quiz
                    </strong>

                    <p>
                        ${escapeHTML(
                            error.message
                        )}
                    </p>

                </div>
                `;

        }


        finally {

            generateQuizBtn.disabled =
                false;

            generateQuizBtn.textContent =
                "🧠 Generate Quiz";

        }

    }
);


// ==========================================
// DISPLAY QUIZ QUESTION
// ==========================================

function displayQuizQuestion() {

    if (
        currentQuestion >=
        currentQuiz.length
    ) {

        showQuizResult();

        return;

    }


    const question =
        currentQuiz[currentQuestion];


    let optionsHTML = "";


    question.options.forEach(
        function(option, index) {


            optionsHTML +=

                `
                <button
                    class="quiz-option"
                    onclick="selectAnswer(${index})">

                    ${String.fromCharCode(
                        65 + index
                    )}.

                    ${escapeHTML(option)}

                </button>
                `;

        }
    );


    quizResult.innerHTML =

        `

        <div class="question-card">

            <p class="question-number">

                Question
                ${currentQuestion + 1}
                of
                ${currentQuiz.length}

            </p>


            <h3>

                ${escapeHTML(
                    question.question
                )}

            </h3>


            <div class="quiz-options">

                ${optionsHTML}

            </div>

        </div>

        `;

}


// ==========================================
// SELECT ANSWER
// ==========================================

function selectAnswer(selectedIndex) {

    const question =
        currentQuiz[currentQuestion];


    const optionButtons =
        document.querySelectorAll(
            ".quiz-option"
        );


    optionButtons.forEach(
        function(button) {

            button.disabled = true;

        }
    );


    if (
        selectedIndex ===
        question.answer
    ) {

        quizScore++;

        optionButtons[
            selectedIndex
        ].classList.add(
            "correct"
        );

    }

    else {

        optionButtons[
            selectedIndex
        ].classList.add(
            "wrong"
        );


        optionButtons[
            question.answer
        ].classList.add(
            "correct"
        );

    }


    setTimeout(
        function() {

            currentQuestion++;

            displayQuizQuestion();

        },
        1000
    );

}


// ==========================================
// QUIZ RESULT
// ==========================================

function showQuizResult() {

    quizCompleted = true;


    const total =
        currentQuiz.length;


    const percentage =
        Math.round(
            (quizScore / total) * 100
        );


    quizzesCount.textContent = "1";

    averageScore.textContent =
        percentage + "%";


    quizResult.innerHTML =

        `

        <div class="quiz-final">

            <div class="quiz-trophy">
                🏆
            </div>

            <h2>
                Quiz Completed!
            </h2>

            <p class="final-score">

                ${quizScore}
                /
                ${total}

            </p>

            <p>

                Your Score:
                <strong>
                    ${percentage}%
                </strong>

            </p>


            <button
                class="ai-btn"
                onclick="restartQuiz()">

                🔄 Try Again

            </button>

        </div>

        `;

}


// ==========================================
// RESTART QUIZ
// ==========================================

function restartQuiz() {

    currentQuestion = 0;

    quizScore = 0;

    quizCompleted = false;

    displayQuizQuestion();

}


// ==========================================
// FORMAT SUMMARY
// ==========================================

function formatSummary(text) {

    let formatted =
        escapeHTML(text);


    formatted =
        formatted.replace(
            /SUMMARY:/g,
            "<h3>📝 Summary</h3>"
        );


    formatted =
        formatted.replace(
            /IMPORTANT POINTS:/g,
            "<h3>📌 Important Points</h3>"
        );


    formatted =
        formatted.replace(
            /KEY CONCEPTS:/g,
            "<h3>🧠 Key Concepts</h3>"
        );


    formatted =
        formatted.replace(
            /CONCLUSION:/g,
            "<h3>🎯 Conclusion</h3>"
        );


    formatted =
        formatted.replace(
            /\n/g,
            "<br>"
        );


    return formatted;

}


// ==========================================
// ESCAPE HTML
// ==========================================

function escapeHTML(text) {

    const div =
        document.createElement("div");


    div.textContent =
        text;


    return div.innerHTML;

}


// ==========================================
// INITIAL LOAD
// ==========================================

loadArticles();