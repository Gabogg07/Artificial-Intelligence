import time
import sys
import math
from copy import copy, deepcopy


def printGrid(g):
    s = ''
    for i in range(0, len(g)):
        for j in range(0, len(g)):
            s = s + str(g[i][j])
        if i < len(g) - 1:
            s = s + '\n'
    print(s)

def generator(state):
    num_rows = state.nbr
    for direction in ("U", "D", "L", "R"):
        for k in range(1, num_rows):
            for a in range(0, num_rows):
                new_state = deepcopy(state)
                for b in range(0, num_rows):
                    if direction == "U":
                        new_state.grid[b - k][a] = state.grid[b][a]
                    elif direction == "D":
                        new_state.grid[((b + k) % num_rows)][a] = state.grid[b][a]
                    elif direction == "L":
                        new_state.grid[a][b - k] = state.grid[a][b]
                    elif direction == "R":
                        new_state.grid[a][((b + k) % num_rows)] = state.grid[a][b]
                yield direction + str(k) + " - (" + str(a) + ")", new_state


class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

    def __str__(self):
        s = ''
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j])
            if i < self.nbr - 1:
                s = s + '\n'
        return s


grid = [[1,0,0], [1, 1, 1],[0,0,0]]
state = State(grid)

print(state)


print("CHANGED GRIDS")
for action, state in generator(state):
    print("Action {0}".format(action))
    printGrid(state.grid)
    print("------------------------")