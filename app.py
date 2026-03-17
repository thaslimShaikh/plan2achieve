from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Serper API key
SERPER_API_KEY = "095815c46b3f6e0860985100651ccf740b9d995a"


def generate_plan(goal, days):

    query = f"how to {goal}"

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

            # remove truncated endings
            snippet = snippet.replace("...", "")
            snippet = snippet.replace("..", "")

            sentences = snippet.split(". ")

            for s in sentences:

                clean = s.strip()

                # filter short / weird sentences
                if len(clean) > 20 and len(clean) < 100:

                    # remove questions and odd text
                    if "?" not in clean and ":" not in clean:

                        steps.append(clean)

    if len(steps) == 0:
        raise Exception("No usable steps returned")

    tasks = []

    for i in range(days):

        step = steps[i % len(steps)]

        # ensure sentence ends properly
        if not step.endswith("."):
            step += "."

        tasks.append(f"Day {i+1}: {step}")

    return tasks


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/goalsetup")
def goalsetup():
    nickname = request.args.get("nickname")
    return render_template("goalsetup.html", nickname=nickname)


@app.route("/dashboard")
def dashboard():

    nickname = request.args.get("nickname", "Friend")
    goal = request.args.get("goal", "")
    category = request.args.get("category", "")
    days = request.args.get("days")

    tasks = []

    if days:
        days = int(days)
        tasks = generate_plan(goal, days)

    total_tasks = len(tasks)

    return render_template(
        "dashboard.html",
        nickname=nickname,
        goal=goal,
        tasks=tasks,
        total=total_tasks,
        remaining=total_tasks
    )


@app.route("/history")
def history():
    return render_template("history.html")


if __name__ == "__main__":
    app.run(debug=True)