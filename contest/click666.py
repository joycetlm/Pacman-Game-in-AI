# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DoubleClick666', second = 'DoubleClick666'):
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
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DoubleClick666(CaptureAgent):
  capsuleTime = 0

  # isTimerTracker=True
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.predictInferences = {i: InferenceFilter(gameState, self.index, i) for i in self.getOpponents(gameState)}
    self.foodNum = 0
    self.foodLeft = len(self.getFood(gameState).asList())

  def chooseAction(self, gameState):
    optAction = None
    maxTemp = float('-Inf')
    for actions in gameState.getLegalActions(self.index):
      for state, action in [(gameState.generateSuccessor(self.index, actions), actions)]:
        if self.evaluate(state, action) > maxTemp:
          maxTemp = self.evaluate(state, action)
          optAction = action

    if DoubleClick666.capsuleTime > 0:
      DoubleClick666.capsuleTime -= 1

      # if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index) in self.getCapsules(gameState):
    for i in self.getCapsules(gameState):
      if gameState.generateSuccessor(self.index, action).getAgentPosition(self.index) == i:
        DoubleClick666.capsuleTime = 40

    # if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index) in self.getFood(gameState).asList():
    for i in self.getFood(gameState).asList():
      if gameState.generateSuccessor(self.index, action).getAgentPosition(self.index) == i:
        self.foodNum += 1
        self.foodLeft -= 1

    if self.redOrBlue(gameState) == 0.0:
      self.foodNum = 0
    return optAction

  def evaluate(self, gameState, action):
    width = gameState.data.layout.width
    height = gameState.data.layout.height

    featureMinFood = 0.0
    minDisFood = float('Inf')
    foodList = self.getFood(gameState).asList()
    for fPosition in foodList:
      tempDisMinFood = self.getMazeDistance(gameState.getAgentPosition(self.index), fPosition)
      if minDisFood > tempDisMinFood:
        minDisFood = tempDisMinFood
    featureMinFood = 1.0 / minDisFood

    featureCapValue = 0.0
    disCap = float('Inf')
    CapList = self.getCapsules(gameState)
    if len(CapList) == 0:
      featureCapValue = 50.0
    else:
      for capPosition in CapList:
        tempDisCap = self.getMazeDistance(gameState.getAgentPosition(self.index), capPosition)
        if disCap > tempDisCap:
          disCap = tempDisCap
      featureCapValue = 1.0 / disCap

    featureEatGhost = 0.0
    if self.capsuleTime > 0:
      if self.redOrBlue(gameState) == 0:
        featureEatGhost = 0.0
      else:
        minDisGhost = float('Inf')
        for i in self.predictInferences:
          enemy = self.predictInferences[i].predictPosition()
          if minDisGhost > self.getMazeDistance(gameState.getAgentPosition(self.index), enemy):
            minDisGhost = self.getMazeDistance(gameState.getAgentPosition(self.index), enemy)
        featureEatGhost = 1.0 / minDisGhost

    featureOpp = (1.0 / (10 * self.capsuleTime) if self.capsuleTime > 0 else 1.0) * self.redOrBluePos(gameState, min(
      [self.predictInferences[i].predictPosition() for i in self.predictInferences],
      key=lambda x: self.getMazeDistance(gameState.getAgentPosition(self.index), x))) * 1.0 / (1 + min(
      [self.getMazeDistance(gameState.getAgentPosition(self.index), self.predictInferences[i].predictPosition()) for i
       in self.predictInferences]))

    paSideValue = 0.0
    parDisValue = 0.0
    featureParValue = 0.0
    for indexSelf in self.getTeam(gameState):
      if indexSelf != self.index:
        parPosition = gameState.getAgentPosition(indexSelf)
        paSideValue = self.redOrBluePos(gameState, parPosition)
        parDisValue = self.getMazeDistance(parPosition, gameState.getAgentPosition(self.index))
    featureParValue = (1.0 - paSideValue) * (1.0 / (1 + parDisValue))

    featureFaceEnemy = 0.0
    if self.capsuleTime > 0:
      featureFaceEnemy = -1.0
    else:
      if self.redOrBlue(gameState) == 0:
        featureFaceEnemy = 0.0
      else:
        for i in self.predictInferences:
          enemy = self.predictInferences[i].predictPosition()
          if 1.5 >= self.getMazeDistance(gameState.getAgentPosition(self.index), enemy):
            featureFaceEnemy = 1.0

    # for i in self.getTeam(gameState):
    #   if i != self.index:
    #     parPosition = gameState.getAgentPosition(i)

    featureGetCap = 0.0
    if self.capsuleTime > 0:
      featureGetCap = 1.0

    featureOneWay = 0.0
    if len(gameState.getLegalActions(self.index)) <= 2:
      featureOneWay = 1.0

    featureEatFood = 0.0
    tempDisPo = float('Inf')
    if self.redOrBlue(gameState) == 0:
      featureEatFood = self.foodNum

    featureFoodProtect = 0.0
    if self.redOrBlue(gameState) == 0:
      featureFoodProtect = 0.0
    else:
      selfPosition = gameState.getAgentPosition(self.index)
      for position in [(width / 2, i) for i in range(1, height) if not gameState.hasWall(width / 2, i)]:
        if tempDisPo > self.distancer.getDistance(selfPosition, position):
          tempDisPo = self.distancer.getDistance(selfPosition, position)
      featureFoodProtect = tempDisPo * self.foodNum

    featureStopValue = 0.0
    if action == Directions.STOP:
      featureStopValue = 1.0

    features = {
      'minDisFood': featureMinFood,
      'capsules':   featureCapValue,
      'opponent':   featureOpp,
      'eatGhost':   featureEatGhost,
      'score':      gameState.getScore(),
      'ally':       featureParValue,
      'faceEnemy':  featureFaceEnemy,
      'getCap':     featureGetCap,
      'oneWay':     featureOneWay,
      'protect':    featureFoodProtect,
      'eatFood':    featureEatFood,
      'stop':       featureStopValue
    }

    weights = {
      'minDisFood': 10.0,
      'opponent':   8.0,
      'eatGhost':   15.0,
      'score':      1000.0,
      'ally':      -1.0,
      'capsules':   20.0,
      'faceEnemy': -1000000.0,
      'getCap':     1000000.0,
      'oneWay':    -100.0,
      'protect':   -0.01,
      'eatFood':    100.0,
      'stop':      -100.0
    }

    for i in self.predictInferences:
      self.predictInferences[i].elapse(gameState)
      self.predictInferences[i].observe(gameState)

    return sum([weights[i] * features[i] for i in features])

  def redOrBluePos(self, gameState, position):
    width = gameState.data.layout.width
    if self.index % 2 == 1:
      if position[0] < width / (2):
        return -1.0
      else:
        return 1.0
    else:
      if position[0] > width / 2:
        return -1.0
      else:
        return 1.0

  def redOrBlue(self, gameState):
    width = gameState.data.layout.width
    position = gameState.getAgentPosition(self.index)
    if self.index % 2 == 1:
      if position[0] < width / (2):
        return 1.0
      else:
        return 0.0
    else:
      if position[0] > width / 2 - 1:
        return 1.0
      else:
        return 0.0


class InferenceFilter:
  def __init__(self, gameState, ourTeam, enemy):
    self.beliefs = util.Counter()
    width = gameState.data.layout.width
    height = gameState.data.layout.height
    for x in range(width):
      for y in range(height):
        if not gameState.hasWall(x, y):
          self.beliefs[(x, y)] = 1.0
    self.beliefs.normalize()
    self.enemy = enemy
    self.index = ourTeam

  def predictPosition(self):
    return self.beliefs.argMax()

  def observe(self, gameState):
    enemyPosition = gameState.getAgentPosition(self.enemy)
    noisyDistance = gameState.getAgentDistances()[self.enemy]
    if enemyPosition:
      for position in self.beliefs:
        if position == enemyPosition:
          self.beliefs[position] = 1.0
        else:
          self.beliefs[position] = 0.0
    else:
      for position in self.beliefs:
        distance = util.manhattanDistance(position, gameState.getAgentPosition(self.index))
        tempBelief = self.beliefs[position]
        probDis = gameState.getDistanceProb(distance, noisyDistance)
        self.beliefs[position] = tempBelief * probDis
      self.beliefs.normalize()

  def elapse(self, gameState):
    tempBeliefs = util.Counter()

    for position in self.beliefs:
      if self.beliefs[position] > 0:
        nextStep = {}
        x, y = position
        if not gameState.hasWall(x - 1, y + 0):
          nextStep[(x - 1, y + 0)] = 1
        if not gameState.hasWall(x + 0, y + 0):
          nextStep[(x + 0, y + 0)] = 1
        if not gameState.hasWall(x + 1, y + 0):
          nextStep[(x + 1, y + 0)] = 1
        if not gameState.hasWall(x + 0, y - 1):
          nextStep[(x + 0, y - 1)] = 1
        if not gameState.hasWall(x + 0, y + 1):
          nextStep[(x + 0, y + 1)] = 1
        stepProbability = 1.0 / len(nextStep)
        for next in nextStep:
          tempBeliefs[next] += stepProbability * self.beliefs[position]
    tempBeliefs.normalize()
    self.beliefs = tempBeliefs
    if self.beliefs.totalCount() <= 0.0:
      width = gameState.data.layout.width
      height = gameState.data.layout.height
      for x in range(width):
        for y in range(height):
          if not gameState.hasWall(x, y):
            self.beliefs[(x, y)] = 1.0
            # self.beliefs[(x,y)]=0.0 if gameState.hasWall(i,j) else 1.0
      self.beliefs.normalize()

