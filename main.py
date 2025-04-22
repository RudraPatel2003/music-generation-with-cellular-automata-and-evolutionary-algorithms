from moviepy import ImageClip, AudioFileClip
from cellular_automata.cellular_automata import CellularAutomata
from music_player.music_player import MusicPlayer
import json
import argparse
import os
import shutil

DEFAULT_VALUES = {"width": 15, "steps": 100, "neighbor_size": 2}
DEFAULT_FILE_NAME = "cellular_automata"
OUTPUT_DIR = "output"


def generate_mp4(mp3_path, png_path, output_path):
    image = ImageClip(png_path)
    audio = AudioFileClip(mp3_path)

    image = image.with_duration(audio.duration)

    image = image.with_audio(audio)

    image.write_videofile(output_path, fps=24, codec="libx264")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Cellular Automata",
        description="This script is designed to generate cellular automata",
    )

    parser.add_argument(
        "--input_file", type=str, help="Path to input json file for reading"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="Path to output json file for writing (required)",
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
    png_path = automata.generate_plot_png()

    music_player = MusicPlayer(automata)
    mp3_path = music_player.export_as_mp3()

    json_path = (
        args.output_file
        if args.output_file is not None
        else os.path.join(OUTPUT_DIR, f"{DEFAULT_FILE_NAME}.json")
    )
    automata.export_as_json(json_path)

    mp4_path = (
        args.output_file
        if args.output_file is not None
        else os.path.join(OUTPUT_DIR, f"{DEFAULT_FILE_NAME}.mp4")
    )
    generate_mp4(mp3_path, png_path, mp4_path)


if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)

    try:
        main()
    finally:
        shutil.rmtree("temp")
