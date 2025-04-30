import os
import shutil
import json

from flask import Flask, flash, redirect, render_template, request, url_for
from evolution.evolution import generate_cellular_automata_with_evolution
from helpers.helper import (
    NUM_OF_CA,
    UPLOAD_FOLDER,
    generate_cellular_automata,
    get_cellular_automata_files,
    CellularAutomataFiles,
    get_hall_of_fame,
)

app = Flask(__name__)
app.secret_key = "123"  # Needed for flashing messages


def reset_dir():
    shutil.rmtree("static/uploads")

    os.makedirs("temp", exist_ok=True)
    os.makedirs("static/uploads", exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    if not os.path.exists(UPLOAD_FOLDER) or len(os.listdir(UPLOAD_FOLDER)) == 0:
        reset_dir()

        for _ in range(NUM_OF_CA):
            generate_cellular_automata()

    files = get_cellular_automata_files()
    return render_template("index.html", files=files, hall_of_fame=get_hall_of_fame())


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
        generate_cellular_automata_with_evolution(json_data[0], json_data[1])

    return redirect(url_for("index"))


@app.route("/clear", methods=["GET"])
def clear():
    reset_dir()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
