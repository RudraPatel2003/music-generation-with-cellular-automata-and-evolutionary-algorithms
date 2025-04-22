import os

from werkzeug.utils import secure_filename

from flask import Flask, flash, redirect, render_template, request, url_for
from remixer import remix_videos

app = Flask(__name__)
app.secret_key = "123"  # Needed for flashing messages

UPLOAD_FOLDER = "static/uploads"


def get_video_list():
    return sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp3")])


@app.route("/", methods=["GET"])
def index():
    videos = get_video_list()
    return render_template("index.html", videos=videos)


@app.route("/submit", methods=["POST"])
def submit():
    selected = request.form.getlist("videos")

    if len(selected) != 2:
        flash("Please select exactly 2 videos.")
        return redirect(url_for("index"))

    video1_path = os.path.join(UPLOAD_FOLDER, secure_filename(selected[0]))
    video2_path = os.path.join(UPLOAD_FOLDER, secure_filename(selected[1]))

    # Get existing video names
    video_names = []
    for f in os.listdir(UPLOAD_FOLDER):
        video_names.append(f)

    # Generate 5 new remixed videos
    remix_videos(video1_path, video2_path, UPLOAD_FOLDER)

    # clear old videos
    for f in video_names:
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
