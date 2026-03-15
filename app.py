from flask import Flask, render_template, request

app = Flask(__name__)

# welcome page
@app.route("/")
def welcome():
    return render_template("welcome.html")


# goal setup page
@app.route("/goalsetup")
def goalsetup():
    nickname = request.args.get("nickname")
    return render_template("goalsetup.html", nickname=nickname)


# dashboard page
@app.route("/dashboard")
def dashboard():

    nickname = request.args.get("nickname")
    goal = request.args.get("goal")
    category = request.args.get("category")
    days = int(request.args.get("days"))

    tasks = []

    task_templates = [
        "Understand your goal",
        "Plan the approach",
        "Prepare resources",
        "Take action towards the goal",
        "Review your progress",
        "Improve your approach",
        "Execute the main step",
        "Reflect on today's effort"
    ]

    for i in range(days):
        task = task_templates[i % len(task_templates)]
        tasks.append(f"Day {i+1}: {task}")

    total_tasks = len(tasks)
    completed_tasks = 0
    remaining_tasks = total_tasks
    consistency = 0

    return render_template(
        "dashboard.html",
        nickname=nickname,
        goal=goal,
        category=category,
        tasks=tasks,
        total=total_tasks,
        completed=completed_tasks,
        remaining=remaining_tasks,
        consistency=consistency
    )


if __name__ == "__main__":
    app.run(debug=True)