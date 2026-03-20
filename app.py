from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import requests
import re
from model.predict import predict_category

app = Flask(__name__)
app.secret_key = "secret123"


# ================= DATABASE =================

def get_db():
    return sqlite3.connect("database.db")


# ================= SERPER API =================

SERPER_API_KEY = "095815c46b3f6e0860985100651ccf740b9d995a"


def generate_plan(goal, days):

    query = f"{goal} daily tasks checklist what to do each day actionable steps"

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"q": query}

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    steps = []

    # ================= CLEANING =================
    for item in data.get("organic", []):
        snippet = item.get("snippet", "")

        if not snippet:
            continue

        sentences = re.split(r"[.]", snippet)

        for s in sentences:
            s = s.strip()

            # remove numbering
            s = re.sub(r"^\(?\d+\)?[\.\)]?\s*", "", s)

            # remove step words
            s = re.sub(r"step\s*\d+[:\-]?\s*", "", s, flags=re.IGNORECASE)

            # remove motivational / explanation junk
            if any(word in s.lower() for word in [
                "is key", "is important", "to overcome",
                "this helps", "this will", "more effective",
                "why", "benefits", "importance", "tips",
                "guide", "learn", "example"
            ]):
                continue

            # basic length control
            if len(s.split()) < 5 or len(s.split()) > 18:
                continue

            # must contain action word (NOT start with it)
            if not any(word in s.lower() for word in [
                "review", "write", "study", "practice",
                "prepare", "revise", "organize", "plan",
                "complete", "focus", "read", "make",
                "create", "work", "avoid", "limit",
                "track", "stop", "start"
            ]):
                continue

            s = s.capitalize().strip()

            if not s.endswith("."):
                s += "."

            steps.append(s)

    # remove duplicates
    steps = list(dict.fromkeys(steps))

    # ================= FINAL TASKS =================
    tasks = []

    limit = min(len(steps), days)

    for i in range(limit):
        tasks.append(f"Day {i+1}: {steps[i]}")

    return tasks
# ================= ROUTES =================

@app.route("/")
def home():
    return redirect("/login")


# ---------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username,password) VALUES (?,?)",
                (username, password)
            )
            conn.commit()
        except:
            return "User already exists!"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/goalsetup")

        return "Invalid login!"

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------- GOAL SETUP ----------
@app.route("/goalsetup")
def goalsetup():

    if "user" not in session:
        return redirect("/login")

    return render_template("goalsetup.html", nickname=session["user"])


# ---------- ML CATEGORY ----------
@app.route("/predict_category")
def predict_category_api():
    goal = request.args.get("goal", "")

    if goal:
        category = predict_category(goal)
        return jsonify({"category": category})

    return jsonify({"category": ""})


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    goal = request.args.get("goal")
    days = request.args.get("days")

    tasks = []

    if goal and days:
        days = int(days)

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO goals (username, goal, days) VALUES (?, ?, ?)",
            (username, goal, days)
        )

        conn.commit()
        conn.close()

        tasks = generate_plan(goal, days)

    return render_template(
        "dashboard.html",
        nickname=username,
        goal=goal,
        tasks=tasks,
        remaining=len(tasks)
    )


# ---------- HISTORY ----------
@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT goal FROM goals WHERE username=?", (username,))
    goals = cur.fetchall()

    conn.close()

    return render_template("history.html", goals=goals)


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)