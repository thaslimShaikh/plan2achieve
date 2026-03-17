from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "secret123"


# ================= DATABASE =================

def get_db():
    return sqlite3.connect("database.db")


# ================= SERPER API =================

SERPER_API_KEY = "095815c46b3f6e0860985100651ccf740b9d995a"

def generate_plan(goal, days):

    query = f"how to {goal} step by step actionable steps"

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"q": query}

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    steps = []

    for item in data.get("organic", []):
        snippet = item.get("snippet", "")

        if snippet:
            snippet = snippet.replace("...", "")
            sentences = snippet.split(". ")

            for s in sentences:
                s = s.strip()

                if 20 < len(s) < 100 and "?" not in s:
                    if not s.endswith("."):
                        s += "."
                    steps.append(s)

    # remove duplicates
    steps = list(dict.fromkeys(steps))

    # 🚨 IMPORTANT: NO fallback, just handle safely
    if len(steps) == 0:
        return []   # return empty list instead of crashing

    tasks = []
    for i in range(days):
        step = steps[i % len(steps)]
        tasks.append(f"Day {i+1}: {step}")

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

        # SAVE GOAL IN DATABASE
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