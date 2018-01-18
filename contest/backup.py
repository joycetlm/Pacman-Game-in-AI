# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from util import nearestPoint
from game import Directions
import game


# Helper classes and methods for A* Search
class Node:
  def __init__(self, state, action, cost, parent):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent

  def getPath(self):
    if self.parent == None: return []
    path = self.parent.getPath() + [self.action]
    return path

class FoodProblem:
  def __init__(self, gameState, agent):
    self.walls = gameState.getWalls()
    self.startState = gameState
    self.agent = agent
    self.expanded = 0

  def getStartState(self):
    return self.startState

  def getSuccessors(self, state):
    successors = []
    self.expanded += 1
    actions = state.getLegalActions(self.agent.index)
    for action in actions:
      successors.append((state.generateSuccessor(self.agent.index, action), action, 1))
    return successors

  def getCostOfActions(self, actions):
    x, y = self.getStartState().getAgentPosition(self.agent.index)
    cost = 0
    for action in actions:
      # figure out the next state and see whether it's legal
      dx, dy = actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost

  def isGoalState(self, state):
    return self.agent.getFood(state).count() == 0




#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='TopAgent', second='BottomAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class MainAgent(CaptureAgent):
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    if self.red:
      CaptureAgent.registerTeam(self, gameState.getRedTeamIndices())
    else:
      CaptureAgent.registerTeam(self, gameState.getBlueTeamIndices())
    self.goToCenter(gameState)

  def getEnemyPos(self, gameState):
    enemyPos = []
    for enemy in self.getOpponents(gameState):
      pos = gameState.getAgentPosition(enemy)
      if pos != None:
        enemyPos.append((enemy, pos))
    return enemyPos

  def enemyDist(self, gameState):
    pos = self.getEnemyPos(gameState)
    minDist = None
    if len(pos) > 0:
      minDist = float('inf')
      myPos = gameState.getAgentPosition(self.index)
      for i, p in pos:
        dist = self.getMazeDistance(p, myPos)
        if dist < minDist:
          minDist = dist
    return minDist

  def whichTerritory(self, gameState):
    return gameState.getAgentState(self.index).isPacman

  # The A*/heuristic code is my partners
  def aStarSearch(self, problem):
    startNode = Node(problem.getStartState(), None, 0, None)
    if problem.isGoalState(startNode.state): return []
    frontier = util.PriorityQueue()
    frontier.push(startNode, self.heuristic(startNode.state, problem))
    explored = set()
    while True:
      if frontier.isEmpty(): return None
      node = frontier.pop()
      if node.state in explored: continue
      if problem.isGoalState(node.state): return node.getPath()
      explored.add(node.state)
      children = problem.getSuccessors(node.state)
      for (state, action, cost) in children:
        child = Node(state, action, cost + node.cost, node)
        if child.state not in explored:
          frontier.push(child, self.heuristic(child.state, problem))

  def heuristic(self, state, problem):
    position = state.getAgentPosition(self.index)
    foods = self.getFood(state).asList()
    #walls = problem.walls
    heurist = 0
    c = None
    for food in foods:
      x = self.getMazeDistance(food, position)
      if c == None or x < self.getMazeDistance(c, position):
        c = food
    if c == None:
      return heurist
    heurist = self.getMazeDistance(c, position)
    if len(foods) > 1:
      for food in foods:
        if food != c:
          minDist = float('Inf')
          for nxt in foods:
            dist = self.getMazeDistance(food, nxt)
            if nxt != food and dist < minDist:
              minDist = dist
          heurist += minDist
    return heurist

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    agentPos = gameState.getAgentPosition(self.index)
    evaluateType = 'attack'

    if self.atCenter == False:
      evaluateType = 'start'
    if agentPos == self.center and self.atCenter == False:
      self.atCenter = True
      evaluateType = 'attack'
    enemyPos = self.getEnemyPos(gameState)
    if len(enemyPos) > 0:
      for enemyI, pos in enemyPos:
        # If we detect an enemy and are on home turf we go after them and defend home
        if self.getMazeDistance(agentPos, pos) < 6 and not self.whichTerritory(gameState):
          evaluateType = 'defend'
          break
    actions = gameState.getLegalActions(self.index)
    values = [self.evaluate(gameState, a, evaluateType) for a in actions]
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action, evaluateType):
    """
    Computes a linear combination of features and feature weights
    """
    if evaluateType == 'attack':
      features = self.getFeaturesAttack(gameState, action)
      weights = self.getWeightsAttack(gameState, action)
    elif evaluateType == 'defend':
      features = self.getFeaturesDefend(gameState, action)
      weights = self.getWeightsDefend(gameState, action)
    elif evaluateType == 'start':
      features = self.getFeaturesStart(gameState, action)
      weights = self.getWeightsStart(gameState, action)
    return features * weights

  def getFeaturesAttack(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    state = successor.getAgentState(self.index)
    pos = state.getPosition()

    foodList = self.getFood(successor).asList()
    if len(foodList) > 0:  # This should always be True, but better safe than sorry
      minDistance = min([self.getMazeDistance(pos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    distEnemy = self.enemyDist(successor)
    if (distEnemy <= 4):
      features['danger'] = 1
    else:
      features['danger'] = 0

    capsules = self.getCapsules(successor)
    if (len(capsules) > 0):
      minCapsuleDist = min([self.getMazeDistance(pos, capsule) for capsule in capsules])
    else:
      minCapsuleDist = 1
    features['capsuleDist'] = 1.0 / minCapsuleDist

    if action == Directions.STOP: features['stop'] = 1
    reverse = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == reverse: features['reverse'] = 1
    return features

  def getFeaturesDefend(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    state = successor.getAgentState(self.index)
    pos = state.getPosition()

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)

    if len(invaders) > 0:
      distances = [self.getMazeDistance(pos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(distances)

    if action == Directions.STOP:
      features['stop'] = 1
    reverse = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == reverse:
      features['reverse'] = 1
    return features

  def getFeaturesStart(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    state = successor.getAgentState(self.index)
    pos = state.getPosition()

    dist = self.getMazeDistance(pos, self.center)
    features['distToCenter'] = dist
    if pos == self.center:
      features['atCenter'] = 1
    return features

  def getWeightsAttack(self, gameState, action):
    return {'successorScore': 100, 'danger': -400, 'distanceToFood': -1, 'stop': -2000, 'reverse': -20,
            'capsuleDist': 3}

  def getWeightsDefend(self, gameState, action):
    return {'numInvaders': -1000, 'invaderDistance': -50, 'stop': -2000, 'reverse': -20}

  def getWeightsStart(self, gameState, action):
    return {'distToCenter': -1, 'atCenter': 1000}


class TopAgent(MainAgent):
  def goToCenter(self, gameState):
    locations = []
    self.atCenter = False
    x = gameState.getWalls().width / 2
    y = gameState.getWalls().height / 2
    if self.red:
      x = x - 1
    self.center = (x, y)
    maxHeight = gameState.getWalls().height

    for i in xrange(maxHeight - y):
      if not gameState.hasWall(x, y):
        locations.append((x, y))
      y = y + 1

    myPos = gameState.getAgentState(self.index).getPosition()
    minDist = float('inf')
    minPos = None

    for location in locations:
      distance = self.getMazeDistance(myPos, location)
      if distance <= minDist:
        minDist = distance
        minPos = location

    self.center = minPos


class BottomAgent(MainAgent):
  def goToCenter(self, gameState):
    locations = []
    self.atCenter = False
    x = gameState.getWalls().width / 2
    y = gameState.getWalls().height / 2
    if self.red:
      x = x - 1
    self.center = (x, y)

    for i in xrange(y):
      if not gameState.hasWall(x, y):
        locations.append((x, y))
      y = y - 1

    myPos = gameState.getAgentState(self.index).getPosition()
    minDist = float('inf')
    minPos = None

    for location in locations:
      distance = self.getMazeDistance(myPos, location)
      if distance <= minDist:
        minDist = distance
        minPos = location

    self.center = minPos