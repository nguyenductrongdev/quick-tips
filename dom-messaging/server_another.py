from flask import Flask, render_template

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<template_filename>")
def template(template_filename):
    return render_template(template_filename)

app.run(debug=True, port=3107)
