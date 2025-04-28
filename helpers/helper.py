from collections import namedtuple
import os
from cellular_automata.cellular_automata import CellularAutomata
from music_player.music_player import MusicPlayer


UPLOAD_FOLDER = "static/uploads"
DEFAULT_VALUES = {"width": 25, "steps": 50, "neighbor_size": 2}
NUM_OF_CA = 5

CellularAutomataFiles = namedtuple("CellularAutomataFiles", ["mp3", "png", "json"])


def generate_cellular_automata(json_data=None):
    initial_state = None
    rules = None

    if json_data:
        initial_state = json_data["initial_state"]
        rules = json_data["rules"]

    automata = CellularAutomata(
        initial_state=initial_state,
        rules=rules,
        width=DEFAULT_VALUES["width"],
        steps=DEFAULT_VALUES["steps"],
        neighbor_size=DEFAULT_VALUES["neighbor_size"],
    )

    automata.run_simulation()

    music_player = MusicPlayer(automata)

    output_file_name = automata.get_output_file_name()

    output_png_path = os.path.join(UPLOAD_FOLDER, f"{output_file_name}.png")
    output_json_path = os.path.join(UPLOAD_FOLDER, f"{output_file_name}.json")
    output_mp3_path = os.path.join(UPLOAD_FOLDER, f"{output_file_name}.mp3")

    automata.generate_plot_png(output_png_path)
    automata.export_as_json(output_json_path)
    music_player.export_as_mp3(output_mp3_path)


def get_cellular_automata_files():
    videos = []

    for file in os.listdir(UPLOAD_FOLDER):
        if not file.endswith(".mp3"):
            continue

        mp3_path = file
        png_path = file.replace(".mp3", ".png")
        json_path = file.replace(".mp3", ".json")

        videos.append(CellularAutomataFiles(mp3=mp3_path, png=png_path, json=json_path))

    return videos
