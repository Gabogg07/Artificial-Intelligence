'''NAMES OF THE AUTHOR(S): Michael Saint-Guillain <michael.sait@uclouvain.be>, Francois Aubry'''
import time
import sys
import math
from functools import *

from search import *
from copy import copy, deepcopy
import datetime

#################
# Problem class #
#################
now = datetime.datetime.now()


class Kubmic(Problem):
    '''def successor(self, state):
        num_rows = state.nbr
        skip = True
        for direction in ("V", "H"):
            for k in range(1, num_rows):
                for a in range(0, num_rows):
                    skip = True
                    new_state = deepcopy(state)
                    for b in range(0, num_rows):
                        if direction == "V":
                            new_state.grid[b - k][a] = state.grid[b][a]
                        elif direction == "H":
                            new_state.grid[a][b - k] = state.grid[a][b]
                        if skip and (direction == 'V') and (b < (len(state.grid) - 1) and state.grid[b][a] != state.grid[b - 1][a]) or (direction == 'H') and (b < (len(state.grid) - 1) and state.grid[a][b] != state.grid[a][b - 1]) or False:
                            skip = False
                    if skip:
                        continue
                    elif direction == "V":
                        if num_rows - k < 0:
                            s = "↓ Col " + str(a + 1) + ": -"
                        else:
                            s = "↑ Col " + str(a + 1) + ": +"
                    elif direction == "H":
                        if num_rows - k < 0:
                            s = "← Row " + str(a + 1) + ": -"
                        else:
                            s = "→ Row " + str(a + 1) + ": +"
                    yield s + str(k), new_state'''

    def successor(self, state):
        for direction in ("V", "H"):
            for k in range(1, state.nbr):
                for a in range(0, state.nbr):
                    new_state = deepcopy(state)
                    if len(\
                            [b for b in range(0, state.nbr) \
                             if (direction == 'V') and (b < (len(state.grid) - 1) and state.grid[b][a] != state.grid[b - 1][a]) or \
                                             (direction == 'H') and (b < (len(state.grid) - 1) and state.grid[a][b] != state.grid[a][b - 1])]) == 0:
                        break
                    for b in range(0, state.nbr):
                        if direction == "V":
                            new_state.grid[b - k][a] = state.grid[b][a]
                        elif direction == "H":
                            new_state.grid[a][b - k] = state.grid[a][b]
                    if direction == "V":
                        if state.nbr - k < 0:
                            s = "↓ Col " + str(a + 1) + ": -"
                        else:
                            s = "↑ Col " + str(a + 1) + ": +"
                    else:
                        if state.nbr - k < 0:
                            s = "← Row " + str(a + 1) + ": -"
                        else:
                            s = "→ Row " + str(a + 1) + ": +"
                    yield s + str(k), new_state




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
        return str(self.grid) == str(other.grid)

    def __hash__(self):
        return hash(str(self.grid))


class Result:
    def __init__(self, goal_node, num_visited_nodes):
        self.goal_node = goal_node
        self.num_visited_nodes = num_visited_nodes

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

grid_init, grid_goal = readInstanceFile("/Users/stefanosambruna/PycharmProjects/AIassignment1/instances/a01")
init_state = State(grid_init)
goal_state = State(grid_goal)
print('-- a04 --')
print('Instance:')
print(init_state)
print('\nGoal:')
print(goal_state)

problem = Kubmic(init_state, goal_state)

# example of bfs graph search
node = breadth_first_graph_search(problem)
if node == None:
    print("No solution found!")
    quit()
# example of print
path = node.path()
path.reverse()


''' 
                                    if direction == "V":
                        if num_rows - k < 0:
                            s = "↓ Col " + str(a + 1) + ": -"
                        else:
                            s = "↑ Col " + str(a + 1) + ": +"
                    else:
                        if num_rows - k < 0:
                            s = "← Row " + str(a + 1) + ": -"
                        else:
                            s = "→ Row " + str(a + 1) + ": +"


'''

then = datetime.datetime.now()
print('\nSolution: ')
print('- Number of moves: ' + str(node.depth))
print("- Duration: " + str(then-now))

for n in path[1:]:
    print()
    print(n)
