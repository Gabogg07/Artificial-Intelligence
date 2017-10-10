'''NAMES OF THE AUTHOR(S): Stefano Sambruna <stefano.sambruna@student.uclouvain>, Gabriel <>'''
import time
import sys
import math
from functools import *

from search import *
from copy import deepcopy
import datetime

#################
# Problem class #
#################
now = datetime.datetime.now()


class Kubmic(Problem):

    def successor(self, state):
        for direction in ("V", "H"):
            for space in range(1, state.nbr):
                for a in range(0, state.nbr):
                    skip = True
                    new_state = deepcopy(state)
                    for b in range(1, state.nbr):
                        if ((direction == 'V') and state.grid[b][a] != state.grid[b - 1][a]) or ((direction == 'H') and state.grid[a][b] != state.grid[a][b - 1]):
                            skip = False
                            break
                    if skip: continue
                    for b in range(0, state.nbr):
                        if direction == "V": new_state.grid[b - space][a] = state.grid[b][a]
                        elif direction == "H": new_state.grid[a][b - space] = state.grid[a][b]
                    if direction == "V": action = "Col " + str(a + 1) + ": "
                    else: action = "Row " + str(a + 1) + ": "
                    if state.nbr - space < 0: action += "-"
                    else: action += "+"
                    action += str(space)
                    yield action, new_state


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

def add_into_the_fringe(fringe, element, closed):
    fringe.append(element)
    closed[element] = True

def bidirectiona_breadth_search(problem, qi, qg):
    closed = {}
    qi.append(problem.initial)
    closed[problem.initial] = True
    qg.append(problem.goal)
    closed[problem.goal] = True



#####################
# Launch the search #
#####################

grid_init, grid_goal = readInstanceFile(sys.argv[1])
#grid_init, grid_goal = readInstanceFile("/Users/stefanosambruna/PycharmProjects/AIassignment1/instances/a01")
init_state = State(grid_init)
goal_state = State(grid_goal)
# print('- Instance: --')
# print(init_state)
# print('')
# print(goal_state)
# print('--------------')

problem = Kubmic(init_state, goal_state)

# example of bfs graph search
node = iterative_deepening_search(problem)

# example of print
path = node.path()
path.reverse()


def comments(comm):
    return '\033[1;36;40m' + comm + '\033[0m'

then = datetime.datetime.now()
#print("- Duration: " + str(then-now))
#print('Number of moves: ' + str(node.depth))
print(comments(
        '\u2193 init'))  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
print(path[0].state)  # assuming that the __str__ function of state outputs the correct format
print()
for n in path[1:]:
    print(comments(
        '\u2193 ' + n.action))  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()


