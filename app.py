from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/goalsetup")
def goalsetup():
    nickname = request.args.get("nickname")
    return render_template("goalsetup.html", nickname=nickname)

@app.route("/dashboard")
def dashboard():
    nickname = request.args.get("nickname")
    return render_template("dashboard.html", nickname=nickname)

if __name__ == "__main__":
    app.run(debug=True)