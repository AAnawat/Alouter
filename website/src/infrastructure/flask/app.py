from flask import Flask, redirect, render_template, request
from ...controllers.routerController import RouterController
from ..mongoDB.client import router_db
import math
from datetime import datetime

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
    try:
        routers = routerController.getAllRouters() or []
        routers_list = list(routers)
        return render_template("home.html", routers=routers_list)
    except Exception as e:
        app.logger.error(f"Error fetching routers for homePage: {e}")
        return render_template("home.html", routers=[])


@app.route("/add-router", methods=["POST"])
def addRouter():
    try:
        name = request.form.get("name")
        host = request.form.get("host")
        username = request.form.get("username")
        password = request.form.get("password")

        if (not name) or (not host) or (not username) or (not password):
            raise ValueError("All fields are required.")

        routerController.addRouter(name, host, username, password)
        return redirect("/")
    except Exception as e:
        app.logger.error(f"Error adding router: {e}")
        try:
            routers = list(routerController.getAllRouters() or [])
        except Exception:
            routers = []
        return render_template("home.html", routers=routers)


@app.route("/router/<ip>")
def getRouterByHost(ip):
    try:
        router = routerController.getRouterByHost(ip)
        if not router:
            return render_template("router_detail.html", router=None)
        return render_template("router_detail.html", router=router)
    except Exception as e:
        app.logger.error(f"Error getting router data for {ip}: {e}")
        return render_template("router_detail.html", router=None)


@app.route("/router/<ip>/interface_status")
def getInterface_status(ip):
    try:
        interface_data = routerController.getInterface_status(ip)
        return render_template("interface_status.html", interface_data=interface_data)
    except Exception as e:
        app.logger.error(f"Error getting interface_status for {ip}: {e}")
        return render_template("interface_status.html", interface_data=None)


@app.route("/router/<ip>/performance")
def getPerformance(ip):
    try:
        performance_data = routerController.getPerformance(ip)
        if not performance_data:
            return render_template("performance.html", performance_data=None)
        return render_template("performance.html", performance_data=performance_data)
    except Exception as e:
        app.logger.error(f"Error getting performance data for {ip}: {e}")
        return render_template("performance.html", performance_data=None)


@app.route("/router/<ip>/logging")
def getLogging(ip):
    try:
        log_data = routerController.getLogging(ip)
        if not log_data:
            return render_template("logging.html", log_data=None)
        return render_template("logging.html", log_data=log_data)
    except Exception as e:
        app.logger.error(f"Error getting logs data for {ip}: {e}")
        return render_template("logging.html", log_data=None)


@app.route("/router/<ip>/<log_id>")
def getLogDetails(ip, log_id):
    log_id = request.view_args["log_id"]

    try:
        log_details = routerController.getLogDetails(log_id)
        if not log_details:
            return render_template("log_details.html", log_data=None)
        return render_template(
            "log_details.html", log_data={"name": log_id, "data": log_details}
        )
    except Exception as e:
        app.logger.error(f"Error getting log details for {ip} log {log_id}: {e}")
        return render_template("log_details.html", log_data=None)


def bytes_to_human(num):
    if num is None:
        return "N/A"
    num = float(num)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} PB"


def percent_used(used, total):
    try:
        used = float(used)
        total = float(total)
        if total == 0:
            return "N/A"
        return f"{(used/total*100):.1f}%"
    except Exception:
        return "N/A"


# ลงทะเบียนเป็น Jinja filter
app.jinja_env.filters["bytes_human"] = bytes_to_human
app.jinja_env.filters["percent_used"] = percent_used


def format_ts(ts):
    if not ts:
        return "N/A"
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            return ts
    else:
        dt = ts
    return dt.strftime("%-d %b %Y %H:%M")


app.jinja_env.filters["fmt_ts"] = format_ts
