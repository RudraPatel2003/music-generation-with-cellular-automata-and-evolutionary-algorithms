import os
import shutil
import json

from flask import Flask, flash, redirect, render_template, request, url_for, session
from helpers.helper import (
    NUM_OF_CA,
    UPLOAD_FOLDER,
    generate_cellular_automata,
    get_cellular_automata_files,
    CellularAutomataFiles,
)

app = Flask(__name__)
app.secret_key = "123"  # Needed for flashing messages


def reset_dir():
    shutil.rmtree("static")

    os.makedirs("temp", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/uploads", exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    if "visited" not in session:
        reset_dir()

        for _ in range(NUM_OF_CA):
            generate_cellular_automata()

        session["visited"] = True

    files = get_cellular_automata_files()
    return render_template("index.html", files=files)


@app.route("/submit", methods=["POST"])
def submit():
    selected_files = request.form.getlist("videos")

    if len(selected_files) != 2:
        flash("Please select exactly 2 videos.")
        return redirect(url_for("index"))

    json_data = []

    for files in selected_files:
        files = eval(files)

        with open(os.path.join(UPLOAD_FOLDER, files.json), "r") as file:
            data = json.load(file)

        json_data.append(data)

    reset_dir()

    for data in json_data:
        generate_cellular_automata(data)

    for _ in range(3):
        generate_cellular_automata()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
