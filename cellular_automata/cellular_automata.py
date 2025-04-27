import os
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import json

random = np.random.default_rng()

PROBABILITY = [0.5, 0.5]


def get_value(array, index):
    length = len(array)

    if index < 0:
        return array[length - abs(index)]

    if index > length - 1:
        return array[index % (length - 1)]

    return array[index]


def generate_rule_string(neighbor_size):
    rule_strings = [
        "".join(bits) for bits in product("01", repeat=(neighbor_size * 2 + 1))
    ]
    rule_outputs = random.choice([0, 1], size=len(rule_strings), p=PROBABILITY).tolist()

    return {rule: output for rule, output in zip(rule_strings, rule_outputs)}


class CellularAutomata:
    def __init__(
        self,
        rules=None,
        initial_state=None,
        width=100,
        steps=100,
        neighbor_size=2,
    ):
        self.rules = None
        self.initial_state = None
        self.width = width
        self.neighbor_size = neighbor_size
        self.steps = steps
        self.history = np.zeros((steps, width), dtype=int)

        if rules:
            self.rules = rules
        else:
            self.rules = generate_rule_string(self.neighbor_size)

        if initial_state:
            self.initial_state = np.array(initial_state)
        else:
            self.initial_state = random.choice([0, 1], size=width, p=PROBABILITY)

    def run_simulation(self):
        self.history[0] = self.initial_state

        for step in range(1, self.steps):
            prev_state = self.history[step - 1]
            current_state = np.zeros_like(prev_state)

            for i in range(self.width):
                neighborhood = "".join(
                    str(get_value(prev_state, n))
                    for n in range(i - self.neighbor_size, i + self.neighbor_size + 1)
                )

                current_state[i] = self.rules[neighborhood]

            self.history[step] = current_state

    def generate_plot_png(self, output_file_path):
        plt.figure(figsize=(10, 6))
        plt.imshow(self.history.T, cmap="binary_r", interpolation="nearest")

        plt.gca().invert_yaxis()

        plt.axhline(y=5 - 0.5, color="red", linestyle="--", linewidth=2)
        plt.axhline(y=20 + 0.5, color="red", linestyle="--", linewidth=2)

        plt.title("1D Cellular Automaton")
        plt.xlabel("Cell Index")
        plt.ylabel("Time Step")

        plt.savefig(output_file_path)

        return output_file_path

    def as_dict(self):
        return {
            "rules": self.rules,
            "initial_state": self.initial_state.tolist(),
            "width": self.width,
            "neighbor_size": self.neighbor_size,
            "steps": self.steps,
        }

    def get_history(self):
        return self.history.tolist()

    def export_as_json(self, output_file_path):
        with open(output_file_path, "w") as file:
            json.dump(self.as_dict(), file)

        return output_file_path

    def get_output_file_name(self):
        rules_string = "".join(str(value) for value in list(self.rules.values()))
        initial_state_string = "".join(
            str(state) for state in self.initial_state.tolist()
        )

        return f"{rules_string}_{initial_state_string}"
