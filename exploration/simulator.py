import time

import matplotlib.pyplot as plt
import numpy as np


class CellularAutomataSimulator:

    def __init__(self):
        self.seed = np.random.seed(int(time.time()))
        self.number_of_states = 3
        self.radius = 1
        self.neighborhood = 2 * self.radius + 1
        self.dimension = 200
        self.timesteps = 1000

        self.color_palette = np.array(
            [[0, 0, 0], [0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 165, 0]]
        )

    def simulate(self):
        # Initialize the board
        board_seed = np.random.randint(0, self.number_of_states, self.dimension)
        self.board = np.zeros((self.timesteps, self.dimension))
        self.board[0, :] = board_seed

        # Randomly initialize the ruleset
        self.rule_table = [0] * 13
        self.rule_table[0] = 0  # Quiescence
        sb = "0"
        for x in range(1, 13):
            self.rule_table[x] = np.random.randint(0, self.number_of_states)
            sb += str(self.rule_table[x])

        rule_string = sb

        print(f"Rule string: {rule_string}")

        # Step through time updating the board
        for x in range(len(self.board) - 1):
            for y in range(len(self.board[x])):
                self.board[x + 1][y] = int(
                    self.rule_table[int(self.calculate_my_sum(x, y))]
                )

        # Create the associated figure
        fig = plt.figure()
        ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self.color_palette[self.board.astype(int)])
        plt.show()

        return self.board

    def calculate_my_sum(self, r, c):
        row = self.board[r]
        s = 0
        for x in reversed(range(1, self.radius + 1)):
            index = c - x
            if index < 0:
                s += row[len(row) + index]
            else:
                s += row[index]

        for x in range(0, self.radius + 1):
            index = c + x
            if index >= len(row):
                s += row[index - len(row)]
            else:
                s += row[index]

        return s


if __name__ == "__main__":
    simulator = CellularAutomataSimulator()
    board = simulator.simulate()

    print(board)
