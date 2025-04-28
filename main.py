import re
import subprocess
import time
from cellular_automata.cellular_automata import CellularAutomata
from music_player.music_player import MusicPlayer
import json
import argparse
import os
import shutil

DEFAULT_VALUES = {"width": 25, "steps": 50, "neighbor_size": 2}


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Cellular Automata",
        description="This script is designed to generate cellular automata",
    )

    parser.add_argument(
        "--input_file", type=str, help="Path to input json file for reading"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_VALUES["width"],
        help="Number of cells in cellular automata",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=DEFAULT_VALUES["steps"],
        help="Number of time steps the cellular automata runs",
    )
    parser.add_argument(
        "--neighbor_size",
        type=int,
        default=DEFAULT_VALUES["neighbor_size"],
        help="Number of surrounding cells used to determine the next state",
    )

    parser.add_argument(
        "--run",
        action="store_true",
        help="Show the png and play mp3 after run",
    )

    return parser.parse_args()


def get_output_dir():
    largest_n = -1
    pattern = re.compile(r"output_(\d+)$")

    for filename in os.listdir("output"):
        match = pattern.match(filename)
        if match:
            n = int(match.group(1))
            if n > largest_n:
                largest_n = n

    return os.path.join("output", f"output_{largest_n + 1}")


def run_and_show_cellular_automata(png_path, mp3_path):
    with open(os.devnull, 'w') as devnull:
        image_proc = subprocess.Popen(["feh", png_path], stdout=devnull, stderr=devnull)
        music_proc = subprocess.Popen(["mpg123", mp3_path], stdout=devnull, stderr=devnull)

    try:
        while True:
            retcode = image_proc.poll()
            if retcode is not None:
                music_proc.terminate()
                break

            if music_proc.poll() is not None:
                break

            time.sleep(0.1)
    finally:
        image_proc.terminate()
        music_proc.terminate()


def main():
    args = parse_arguments()

    rules = None
    initial_state = None
    width = None
    steps = None
    neighbor_size = None

    if args.input_file:
        with open(args.input_file, "r") as file:
            data = json.load(file)

        rules = data["rules"]
        initial_state = data["initial_state"]
        width = data.get("width", args.width)
        steps = data.get("steps", args.width)
        neighbor_size = data.get("neighbor_size", args.width)

    else:
        width = args.width
        steps = args.steps
        neighbor_size = args.neighbor_size

    automata = CellularAutomata(
        rules=rules,
        initial_state=initial_state,
        width=width,
        steps=steps,
        neighbor_size=neighbor_size,
    )

    automata.run_simulation()
    output_dir = get_output_dir()

    os.makedirs(output_dir, exist_ok=True)

    png_path = automata.generate_plot_png(output_dir)
    json_path = automata.export_as_json(output_dir)

    music_player = MusicPlayer(automata)
    mp3_path = music_player.export_as_mp3(output_dir)

    print(f"graph.png: {png_path}")
    print(f"Metadata.json: {json_path}")
    print(f"song.mp3: {mp3_path}")

    if args.run:
        run_and_show_cellular_automata(png_path, mp3_path)


if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        main()
    finally:
        shutil.rmtree("temp")
