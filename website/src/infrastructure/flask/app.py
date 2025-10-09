from flask import Flask, render_template


app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="templates")

@app.route('/')
def homePage():
    return render_template("home.html")