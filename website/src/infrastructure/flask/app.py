from flask import Flask, redirect, render_template, request
from ...controllers.routerController import RouterController
from ..mongoDB.client import router_db

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)
routerController = RouterController(router_db)


@app.route("/health-check")
def healthCheckAPI():
    return {"status": "Running"}


@app.route("/")
def homePage():
    return render_template("home.html")

@app.route('/add-router', methods=['POST'])
def addRouter():
    try:
        name = request.form.get('name')
        host = request.form.get('host')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (not name) or (not host) or (not username) or (not password):
            raise ValueError("All fields are required.")

        routerController.addRouter(name, host, username, password)
        return redirect('/')
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
