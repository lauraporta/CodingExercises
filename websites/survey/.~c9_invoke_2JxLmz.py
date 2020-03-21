import cs50
import csv

from flask import Flask, abort, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("email") or not request.form.get("address") or not request.form.get("city") or not request.form.get("region") or not request.form.get("cap"):
        return render_template("error.html", message="Qualcosa è andato storto. Si prega di tornare indietro e ricompilare il modulo.")

    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("email"), request.form.get("address"),
                     request.form.get("city"), request.form.get("region"), request.form.get("cap")))
    file.close()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    try:
        file = open("survey.csv", "r")
    except Exception:
        return render_template("error.html", message="Impossibile aprire il file.")
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    peopleData = list(reader)
    return render_template("sheet.html", peopleData=peopleData)