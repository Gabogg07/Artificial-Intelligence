'''NAMES OF THE AUTHOR(S): Michael Saint-Guillain <michael.sait@uclouvain.be>, Francois Aubry'''
import time
import sys
import math
from search import *
from copy import copy, deepcopy


#################
# Problem class #
#################
class Kubmic(Problem):
    def successor(self, state):
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



###############
# State class #
###############

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

    def __eq__(self, other):
        return self.grid == other.grid


###################### 
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    n = math.floor(len(lines) / 2)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(0, m)] for i in range(0, n)]
    grid_goal = [[lines[i][j] for j in range(0, m)] for i in range(n + 1, len(lines))]

    return grid_init, grid_goal


#####################
# Launch the search #
#####################

grid_init, grid_goal = readInstanceFile("/Users/stefanosambruna/PycharmProjects/AIassignment1/instances/a03")
init_state = State(grid_init)
goal_state = State(grid_goal)
print('- Instance: --')
print(init_state)
print('')
print(goal_state)
print('--------------')

problem = Kubmic(init_state, goal_state)

# example of bfs graph search
node = breadth_first_graph_search(problem)

# example of print
path = node.path()
path.reverse()


def comments(comm):
    return '\033[1;36;40m' + comm + '\033[0m'


print('Number of moves: ' + str(node.depth))
print('Here the fucking solution: ')
for n in path:
    '''print(comments(
        '\u2193 ' + n))  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
    print(n.state)  # assuming that the __str__ function of state outputs the correct format'''
    print("---------------------")
    print(n)
