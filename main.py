import threading
from cellular_automata.cellular_automata import CellularAutomata
from music_player.music_player import MusicPlayer
import json
import argparse


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

    parser.add_argument(
        "--play_music",
        action="store_true",
        help="Play the cellular automata as music",
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

    if args.play_music:
        music_player = MusicPlayer(automata)
        music_player.play()

        thread = threading.Thread(target=music_player.play)
        thread.start()

    automata.plot()

    if args.output_file:
        with open(args.output_file, "w") as file:
            json.dump(automata.as_dict(), file)


if __name__ == "__main__":
    main()
