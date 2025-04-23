from cellular_automata.cellular_automata import CellularAutomata
from music_player.music_player import MusicPlayer
import json
import argparse
import os
import shutil

DEFAULT_VALUES = {"width": 15, "steps": 100, "neighbor_size": 2}

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

    return parser.parse_args()


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
    output_dir = automata.get_output_dir()

    os.makedirs(output_dir, exist_ok=True)

    png_path = automata.generate_plot_png(output_dir)
    json_path = automata.export_as_json(output_dir)

    music_player = MusicPlayer(automata)
    mp3_path = music_player.export_as_mp3(output_dir)

    print(f"graph.png: {png_path}")
    print(f"Metadata.json: {json_path}")
    print(f"song.mp3: {mp3_path}")

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        main()
    finally:
        shutil.rmtree("temp")
