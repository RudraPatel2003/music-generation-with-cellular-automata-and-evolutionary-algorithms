import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import json

random = np.random.default_rng()


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
    rule_outputs = random.choice([0, 1], size=len(rule_strings), p=[0.7, 0.3]).tolist()

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
            self.initial_state = random.choice([0, 1], size=width, p=[0.7, 0.3])

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

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.imshow(self.history, cmap="binary", interpolation="nearest")
        plt.title("1D Cellular Automaton")
        plt.xlabel("Cell Index")
        plt.ylabel("Time Step")
        plt.show()

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
