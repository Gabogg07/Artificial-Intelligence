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
                    #TODO: check this
                    if state.nbr - space < 0: action += "-"
                    else: action += "+"
                    action += str(space)
                    yield action, new_state

    def initial_test(self, state):
        return self.initial == state


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

def add_into_the_queue(queue, new_node, closed):
    queue.append(new_node)
    closed[new_node.state] = True

    '''
    
    
            for w in range(0, len(path_to_goal) - 2):
            path_to_bridge[w + 1].parent = path_to_bridge[w]
            path_to_bridge[w].state = deepcopy(path_to_bridge[w + 1])
        path_to_bridge[0].parent = path_to_goal[len(path_to_goal) - 1]
        return path_to_goal[0]'''

def exctractMoveFromAction(action):
    reverse_number_string = ''
    for i in range((len(action) - 1), 0, -1):
        if action[i].isdigit():
            reverse_number_string += action[i]
        else:
            return i, int(reverse_number_string[::-1])


def success(my_problem, goal_node, qi, qg, initial):
    if my_problem.initial == goal_node.state:
        return goal_node.path.reverse()
    elif my_problem.goal == goal_node.state:
        return goal_node.path
    if initial:
        bridge_node = list(filter(lambda e: e.state == goal_node.state, qg.A))[0]
        path_to_goal = bridge_node.path()
        path_to_bridge = goal_node.path()
        path_to_bridge.reverse()

        path_to_goal[1].parent=path_to_bridge[-1]

        for n in range(1,len(path_to_goal)-1):
            path_to_goal[n+1].parent = path_to_goal[n]

        for n in range(len(path_to_goal) - 1, 0, -1):
            path_to_goal[n].action = path_to_goal[n -1].action

        for n in range(1, len(path_to_goal)):
            pos, num = exctractMoveFromAction(path_to_goal[len(path_to_goal) - n].action)
            path_to_goal[len(path_to_goal) - n].action = path_to_goal[len(path_to_goal) - n].action[0:pos + 1] + str(goal_node.state.nbr - num)
        return path_to_goal[-1]
        '''print("PATH TO BRIDGE")
        for n in path_to_bridge:
            print(
                n.action)  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
            print(n.state)  # assuming that the __str__ function of state outputs the correct format
            print()
        print("PATH TO GOAL")
        for n in path_to_goal:
            print(n.action)
            print(n.state)  # assuming that the __str__ function of state outputs the correct format
            print()'''


    else:
        bridge_node = list(filter(lambda e: e.state == goal_node.state, qi.A))[0]
        path_to_goal = goal_node.path()
        path_to_bridge = bridge_node.path().reverse()
        print("PATH TO BRIDGE")
        for n in path_to_bridge:
            print(
                n.action)  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
            print(n.state)  # assuming that the __str__ function of state outputs the correct format
            print()
        print("PATH TO GOAL")
        for n in path_to_goal:
            print(n.action)
            print(n.state)  # assuming that the __str__ function of state outputs the correct format
            print()


def bidirectional_breadth_search(problem, qi, qg):
    inverse_problem = Kubmic(problem.goal, problem.initial)
    closed = {}
    add_into_the_queue(qi, Node(problem.initial), closed)
    add_into_the_queue(qg, Node(problem.goal), closed)
    while qi.__len__() > 0 and qg.__len__() > 0:
        if qi.__len__() > 0:
            node_x = qi.pop()
            if problem.goal_test(node_x.state):
                return node_x
            elif len(list(filter(lambda e: e.state == node_x.state, qg.A))) != 0:
                return success(problem, node_x, qi, qg, True)  #problem,goal_node, qi, qg, initial
            for x in node_x.expand(problem):
                if x.state not in closed:
                    add_into_the_queue(qi, x, closed)
        if qg.__len__() > 0:
            node_x = qg.pop()
            if problem.initial_test(node_x.state):
                return node_x
            elif len(list(filter(lambda e: e.state == node_x.state, qi.A))) != 0:
                return success(problem, node_x, qi, qg, False)
            for x in node_x.expand(inverse_problem):
                if x not in closed:
                    add_into_the_queue(qg, x, closed)
    return print("FAILURE")




            #fringe.extend(node.expand(problem))


#####################
# Launch the search #
#####################

#grid_init, grid_goal = readInstanceFile(sys.argv[1])
grid_init, grid_goal = readInstanceFile("/Users/stefanosambruna/PycharmProjects/AIassignment1/instances/a03")
init_state = State(grid_init)
goal_state = State(grid_goal)
# print('- Instance: --')
# print(init_state)
# print('')
# print(goal_state)
# print('--------------')

problem = Kubmic(init_state, goal_state)

# example of bfs graph search
#node = iterative_deepening_search(problem)
node = bidirectional_breadth_search(problem, FIFOQueue(), FIFOQueue())
# example of print
path = node.path()
path.reverse()


def comments(comm):
    return '\033[1;36;40m' + comm + '\033[0m'

then = datetime.datetime.now()
print("- Duration: " + str(then-now))
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
