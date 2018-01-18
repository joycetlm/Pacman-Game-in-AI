# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import util
class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    if successorGameState.isWin():
      return 999

    if successorGameState.isLose():
      return -999

    score = successorGameState.getScore()

    ghostDistance = []

    for ghost in newGhostStates:
      ghostDistance.append(manhattanDistance(newPos, ghost.getPosition()))

    foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]

    score -= 10.0 / min(ghostDistance)

    if len(foodDistance) > 0:
      score += 10.0 / min(foodDistance)

    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    def minValue(gameState, depth, numGhost):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(numGhost)
      result = float("inf")

      for action in legalActions:
        nextState = gameState.generateSuccessor(numGhost, action)
        if numGhost > 1:
          result = min(result, minValue(nextState, depth, numGhost - 1))
        else:
          result = min(result,maxValue(nextState, depth - 1))

      return result

    def maxValue(gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(0)
      result = float("-inf")

      for action in legalActions:
        nextState = gameState.generateSuccessor(0, action)
        result = max(result, minValue(nextState, depth, gameState.getNumAgents() - 1))

      return result

    legalActions = gameState.getLegalActions(0)
    curValue = float("-inf")
    nextAction = Directions.STOP

    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      nextValue = minValue(nextState, self.depth, gameState.getNumAgents() - 1)

      if nextValue > curValue:
        curValue = nextValue
        nextAction = action

    return nextAction





class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def minValue(gameState, depth, numGhost, alpha, beta):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(numGhost)
      result = float("inf")

      for action in legalActions:
        nextState = gameState.generateSuccessor(numGhost, action)
        if numGhost > 1:
          result = min(result, minValue(nextState, depth, numGhost - 1, alpha, beta))
        else:
          result = min(result,maxValue(nextState, depth - 1, alpha, beta))
        if result <= alpha:
          return result
        beta = min(beta, result)
      return result

    def maxValue(gameState, depth, alpha, beta):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(0)
      result = float("-inf")

      for action in legalActions:
        nextState = gameState.generateSuccessor(0, action)
        result = max(result, minValue(nextState, depth, gameState.getNumAgents() - 1, alpha, beta))
        if result >= beta:
          return result
        alpha = max(alpha, result)

      return result

    legalActions = gameState.getLegalActions(0)
    curValue = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    nextAction = Directions.STOP

    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      nextValue = minValue(nextState, self.depth, gameState.getNumAgents() - 1, alpha, beta)

      if nextValue > curValue:
        curValue = nextValue
        nextAction = action
      if curValue >= beta:
        return nextAction
      alpha = max(alpha, curValue)

    return nextAction


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    def expValue(gameState, depth, numGhost):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(numGhost)
      result = 0
      num = len(legalActions)

      for action in legalActions:
        nextState = gameState.generateSuccessor(numGhost, action)
        #suppose each successor has same probability
        if numGhost > 1:
          result += expValue(nextState, depth, numGhost - 1)
        else:
          result += maxValue(nextState, depth - 1)

      return result/num

    def maxValue(gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      legalActions = gameState.getLegalActions(0)
      result = float("-inf")

      for action in legalActions:
        nextState = gameState.generateSuccessor(0, action)
        result = max(result, expValue(nextState, depth, gameState.getNumAgents() - 1))

      return result

    legalActions = gameState.getLegalActions(0)
    curValue = float("-inf")
    nextAction = Directions.STOP

    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      nextValue = expValue(nextState, self.depth, gameState.getNumAgents() - 1)

      if nextValue > curValue:
        curValue = nextValue
        nextAction = action

    return nextAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  """
  I use currentscore, minimum food distance, current food number, ghost distance, minimum capsule
  distance and current capsule number with the related ghost timer conditions to make a evaluation function
  """
  currentPos = currentGameState.getPacmanPosition()
  capsules = currentGameState.getCapsules()
  capsulesDis = [manhattanDistance(currentPos,capsule) for capsule in capsules]
  currentFood = currentGameState.getFood()
  foodlist= currentFood.asList()
  foodNum = currentGameState.getNumFood()
  foodDistance = [manhattanDistance(currentPos, food) for food in foodlist]
  currentScore = currentGameState.getScore()
  ghostStates = currentGameState.getGhostStates()
  scaredTimers = [ghost.scaredTimer for ghost in ghostStates]
  ghostsDis = [manhattanDistance(currentPos, ghost.getPosition()) for ghost in ghostStates]
     
  if currentGameState.isWin():
      return 999

  if currentGameState.isLose():
      return -999

  score = 0
  minFoodDisScore = 10/min(foodDistance)
  foodNumScore = 1/foodNum
  
  ghostScore = 0
  for i in range(len(ghostStates)):
    if ghostsDis[i] < 3 and scaredTimers[i] < 1:
      ghostScore += 20*ghostsDis[i]
    elif ghostsDis[i] < 3 and scaredTimers[i] >= 1:
      ghostScore += 10*ghostsDis[i]
    else:
      ghostScore += ghostsDis[i]
  ghostScore = 1/ghostScore
  
  capsuleScore = 0
  if len(capsules) > 0 and all(timer == 0 for timer in scaredTimers):
    capsuleScore = 1/min(capsulesDis) - 5*len(capsules)
  elif len(capsules) > 0:
    capsuleScore = 1/min(capsulesDis)
  
  score = currentScore + minFoodDisScore + foodNumScore + ghostScore + capsuleScore
  return score
  

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

