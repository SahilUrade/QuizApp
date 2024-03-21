from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///questions.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    topic = request.form.get("topic")
    if not topic:
        return redirect("/")
    if topic:
        questions = db.execute("SELECT * FROM ? ORDER BY RANDOM() LIMIT 5", topic)
        return render_template("quiz.html", questions=questions, topic=topic)


@app.route("/result", methods=["GET", "POST"])
def result():

    result = []
    for x in range(1, 6):
        a = int(request.form.get("id"+str(x)))
        b = request.form.get("question"+str(x))
        result.append([a, b])

    topic = request.form.get("topic")
    questions = db.execute("SELECT * FROM ?", topic)

    correct = 0
    for x in result:
        for y in questions:
            if x[0] == y["id"]:
                if x[1] == y["answer"]:
                    correct += 1

    return render_template("result.html", correct=correct)
