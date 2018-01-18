# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    fringe = Stack()
    actions = []
    closed = []
    fringe.push((problem.getStartState(), actions, closed))

    while not fringe.isEmpty():
        curState, actions, closed = fringe.pop()
        closed.append(curState)
        for successor, action, stepCost in problem.getSuccessors(curState):
            if successor not in closed:
                if problem.isGoalState(successor):
                    actions.append(action)
                    return actions
                fringe.push((successor, actions + [action], closed))
    return []



    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    stop = Directions.STOP
    fringe = util.Queue()
    startState = problem.getStartState()
    previousState = []
    #store currentstate, all previous states and the route from startstate to currentstate
    fringe.push((startState, []))

    while fringe.isEmpty() == False :
        state, route  = fringe.pop()
        if problem.isGoalState(state) == False:
            if not state in previousState:
                previousState = previousState + [state]
                for (childstate, cdirection, cost) in problem.getSuccessors(state) :
                    newRoute = route + [cdirection]
                    fringe.push((childstate, newRoute))
        elif problem.isGoalState(state):
            return route
    return [stop]
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe = PriorityQueue()
    actions = []
    closed = []
    fringe.push((problem.getStartState(), actions),0)

    while not fringe.isEmpty():
        curState, actions = fringe.pop()
        closed.append(curState)

        if problem.isGoalState(curState):
            return actions

        for successor, action, stepCost in problem.getSuccessors(curState):
            if successor not in closed:
                fringe.push((successor, actions + [action]),problem.getCostOfActions(actions + [action]))
    return []



    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    from game import Directions
    stop = Directions.STOP
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    previousState = []
    scost = heuristic(startState, problem)
    fringe.push((startState, []), scost)

    while fringe.isEmpty() == False :
        state, route = fringe.pop()
        if problem.isGoalState(state) == False:
            if not state in previousState:
                previousState = previousState + [state]
                for (childstate, cdirection, cost) in problem.getSuccessors(state) :
                    newRoute = route + [cdirection]
                    newCost = problem.getCostOfActions(newRoute) + heuristic(childstate, problem)
                    fringe.push((childstate, newRoute), newCost)
        elif problem.isGoalState(state):
            return route
    return [stop]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
