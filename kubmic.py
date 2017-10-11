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
    """
        @:param state: State that is desired to be analyzed to calculate all the possible movements out of it.

        successor function takes a given state and calculates all the possible moves that can be made out of it.
        The moves list consist in a column or row to be moved, a direction (Vertical or Horizontal) and the number of
        steps to be moved.
        For this method the convention used is:
        - Vertical Direction and positive movement means translate up
        - Horizontal Direction and positive movement means translate right
        The method consist in taking each row and outputting all the size "space" movements , where "space" goes from 0
        to the size of the grid. For the column is the same procedure.
    """
    def successor(self, state):
        for direction in ("V", "H"):
            for space in range(1, state.nbr):
                for a in range(0, state.nbr):
                    skip = True
                    new_state = deepcopy(state)
                    #Check to control if there is any row or column made completely of only one character.
                    for b in range(1, state.nbr):
                        if ((direction == 'V') and state.grid[b][a] != state.grid[b - 1][a]) or (
                            (direction == 'H') and state.grid[a][b] != state.grid[a][b - 1]):
                            skip = False
                            break
                    '''If the control before found that the row/column was made entirely of the same character the
                        program skips the creation of all the different states in that direction.'''
                    if skip: continue
                    if direction == "V":
                        for b in range(0, state.nbr):
                            new_state.grid[b - space][a] = state.grid[b][a]
                    elif direction == "H":
                        new_state.grid[a] = new_state.grid[a][new_state.nbr - space:] + new_state.grid[a][
                                                                                        :new_state.nbr - space]
                    if direction == "V":
                        action = "Col " + str(a + 1) + ": "
                    else:
                        action = "Row " + str(a + 1) + ": "
                    action += "+" + str(space)
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

    #Method override to allow comparison between states
    def __eq__(self, other):
        return str(self.grid) == str(other.grid)

    #Method override in order to make a state hashable
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

"""
    @:param queue: Queue where a node is going to be added
    @:param new_node: Node to be added into the queue and closed list.
    @:param closed: Dictionary used for added nodes control.
    The Function adds a node to the end of a queue and to a control dictionary called closed.
"""
def add_into_the_queue(queue, new_node, closed):
    queue.append(new_node)
    closed[new_node.state] = True

"""
    @:param action: String containing a movement
    The function receives a string from where the last number occurrence is extracted and turned into integer.    
"""
def extractMoveFromAction(action):
    reverse_number_string = ''
    for i in range((len(action) - 1), 0, -1):
        if action[i].isdigit():
            reverse_number_string += action[i]
        else:
            return i, int(reverse_number_string[::-1])

"""
    @:param goal_node: Node that was either successful for goal testing or was the search intersection.
    @:param qi: Queue containing all the nodes to be analyzed by the search at the moment of the call, queue for the 
                search that started from the initial node.
    @:param qg: Queue containing all the nodes to be analyzed by the search at the moment of the call, queue for the 
                search that started from the goal node.           
    @:param initial: Boolean that takes true value if the goal_node comes from the goal oriented search, or false 
                     if it comes from the initial oriented search.
    Once having the node that was the connection between the two searches its necessary to merge the path from the
    initial node to it and from that node to the goal. For the initial state oriented search the movements are adapted
    because of the orientation change , and also the parent linking is reversed so it matches de goal oriented search.
"""
def generate_path(my_problem, goal_node, qi, qg, initial):

    if initial:
        print("FROM THE INIT")
        bridge_node = list(filter(lambda e: e.state == goal_node.state, qg.A))[0]
        path_to_goal = bridge_node.path()
        path_to_bridge = goal_node.path()
        path_to_bridge.reverse()
    else:
        print("FROM THE GOAL")
        bridge_node = list(filter(lambda e: e.state == goal_node.state, qi.A))[0]
        path_to_goal = goal_node.path()
        path_to_bridge = bridge_node.path().reverse()

    #Links the path from the initial node to the found node with the path from the node to the goal.
    path_to_goal[1].parent=path_to_bridge[-1]

    #Fixes the parent link in the path from the node to the goal.
    for n in range(1,len(path_to_goal)-1):
        path_to_goal[n+1].parent = path_to_goal[n]

    #Rearranges the actions to fit the goal oriented search.
    for n in range(len(path_to_goal) - 1, 0, -1):
        path_to_goal[n].action = path_to_goal[n -1].action

    #Fixes the number of moves according to the direction of it.
    for n in range(1, len(path_to_goal)):
        pos, num = extractMoveFromAction(path_to_goal[len(path_to_goal) - n].action)
        path_to_goal[len(path_to_goal) - n].action = path_to_goal[len(path_to_goal) - n].action[0:pos + 1] + str(goal_node.state.nbr - num)

    return path_to_goal[-1]


"""
    @:param problem: Problem to be resolved by the search
    @:param qi: Empty FIFOQueue
    @:param qg: Empty FIFOQueue  
    Implementation of the bidirectional search algorithm using the breadth first principle (FIFO queues).
"""
def bidirectional_breadth_graph_search(problem, qi, qg):
    # Creation of the problem that has the initial state as new goal and the old goal as new initial state.
    inverse_problem = Kubmic(problem.goal, problem.initial)
    closed = {}
    add_into_the_queue(qi, Node(problem.initial), closed)
    add_into_the_queue(qg, Node(problem.goal), closed)

    while qi.__len__() > 0 and qg.__len__() > 0:
        if qi.__len__() > 0:
            node_x = qi.pop()

            if problem.goal_test(node_x.state):
                return node_x
            #Checks if the node been analyzed is in the queue of the other search
            elif len(list(filter(lambda e: e.state == node_x.state, qg.A))) != 0:
                return generate_path(problem, node_x, qi, qg, True)  #problem,goal_node, qi, qg, initial
            for x in node_x.expand(problem):
                if x.state not in closed:
                    add_into_the_queue(qi, x, closed)
        if qg.__len__() > 0:
            node_x = qg.pop()

            if problem.initial_test(node_x.state):
                path_to_goal = node_x.path()
                #Fix of the actions to make them fit the goal oriented convention.
                for n in range(1, len(path_to_goal)):
                    pos, num = extractMoveFromAction(path_to_goal[len(path_to_goal) - n].action)
                    path_to_goal[len(path_to_goal) - n].action = path_to_goal[len(path_to_goal) - n].action[
                                                                 0:pos + 1] + str(node_x.state.nbr - num)
                return path_to_goal[-1]


            # Checks if the node been analyzed is in the queue of the other search

            elif len(list(filter(lambda e: e.state == node_x.state, qi.A))) != 0:
                return generate_path(problem, node_x, qi, qg, False)
            for x in node_x.expand(inverse_problem):
                if x not in closed:
                    add_into_the_queue(qg, x, closed)
    return None




            #fringe.extend(node.expand(problem))


#####################
# Launch the search #
#####################


#grid_init, grid_goal = readInstanceFile(sys.argv[1])
grid_init, grid_goal = readInstanceFile("instances/a01")
#grid_init, grid_goal = readInstanceFile("instances/a02")
#grid_init, grid_goal = readInstanceFile("instances/a03")
#grid_init, grid_goal = readInstanceFile("instances/a04")
#grid_init, grid_goal = readInstanceFile("instances/a05")
#grid_init, grid_goal = readInstanceFile("instances/b01")
#grid_init, grid_goal = readInstanceFile("instances/b02")
#grid_init, grid_goal = readInstanceFile("instances/b03")
#grid_init, grid_goal = readInstanceFile("instances/b04")
#grid_init, grid_goal = readInstanceFile("instances/b05")

init_state = State(grid_init)
goal_state = State(grid_goal)
# print('- Instance: --')
# print(init_state)
# print('')
# print(goal_state)
# print('--------------')

problem = Kubmic(init_state, goal_state)

# example of bfs graph search
node = depth_first_graph_search(problem)
#node = bidirectional_breadth_graph_search(problem, FIFOQueue(), FIFOQueue())
# example of print
path = node.path()
path.reverse()


def comments(comm):
    return '\033[1;36;40m' + comm + '\033[0m'

then = datetime.datetime.now()
print("- Duration: " + str(then-now))
print('Number of moves (depth): ' + str(node.depth))
print('Number of moves: ' + str(len(path)-1))

print(comments(
        '\u2193 init'))  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
print(path[0].state)  # assuming that the __str__ function of state outputs the correct format
print()
for n in path[1:]:
    print(comments(
        '\u2193 ' + n.action))  # assuming the comment attribute of state contains a relevant string (e.g. describing the current move)
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
