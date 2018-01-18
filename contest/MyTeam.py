from captureAgents import CaptureAgent
import game
from game import Directions
from game import Agent
import random 
import time
import util

#

def createTeam(firstIndex, secondIndex, isRed,
    first = 'xxxAgent', second = 'xxxAgent'):

  return [eval(first)(firstIndex), eval(second)(secondIndex)]



class xxxAgent(CaptureAgent):
  powerTimer=0
  #isTimerTracker=True
  def registerInitialState(self,gameState):
        CaptureAgent.registerInitialState(self, gameState) 
        self.predictInferences = {i:InferenceFilter(gameState,self.index,i) for i in self.getOpponents(gameState)}

        self.foodNum = 0

  def chooseAction(self,gameState):
    try:
        resultAction=None
        temp= float('-Inf')#0.0
        for actions in gameState.getLegalActions(self.index):
            for state,action in [(gameState.generateSuccessor(self.index,actions),actions)]:
                if self.evaluate(state,action)>temp:
                    temp=self.evaluate(state,action)
                    resultAction=action
        

        if xxxAgent.powerTimer>0:
            xxxAgent.powerTimer-=1
       
        #if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index) in self.getCapsules(gameState):
        for i in self.getCapsules(gameState):
            if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index)==i:
                xxxAgent.powerTimer=40
     
        #if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index) in self.getFood(gameState).asList():
        for i in self.getFood(gameState).asList():
            if gameState.generateSuccessor(self.index,action).getAgentPosition(self.index)==i:
                self.foodNum+=1

        if self.redOrBlue(gameState)==0.0:
            self.foodNum=0
        return resultAction
    except Exception:
        return random.choice(gameState.getLegalActions())


  def evaluate(self,gameState,action):
    width=gameState.data.layout.width
    height=gameState.data.layout.height
    
    resultMinFood=0.0
    minDisFood=9999999.9
    foodList=self.getFood(gameState).asList()
    for fPosition in foodList:
        tempDisMinFood=self.getMazeDistance(gameState.getAgentPosition(self.index),fPosition)
        if minDisFood>tempDisMinFood:
            minDisFood=tempDisMinFood
    resultMinFood=1.0/minDisFood        
    
    capValue=0.0
    disCap=9999999.9
    CapList=self.getCapsules(gameState)
    if len(CapList)==0:
        capValue=100.0
    else:
        for capPosition in CapList:
            tempDisCap=self.getMazeDistance(gameState.getAgentPosition(self.index),capPosition)
            if disCap>tempDisCap:
                disCap=tempDisCap
        capValue=1.0/disCap
        
   
    """
    timeValue=0.0
    if self.powerTimer>0:
        timeValue=1.0/(10*self.powerTimer)
    else:
        timeValue=1.0
    """
    #timeValue=(1.0/(10*self.powerTimer) if self.isPowered() else 1.0)
    """
    disValue=0.0
    tempDisValue=99999.9
    for index in self.predictInferences:
        dis=self.getMazeDistance(gameState.getAgentPosition(self.index),self.predictInferences[index].predictPosition())
        if dis<tempDisValue:
            tempDisValue=dis
    disValue=tempDisValue+1
    """
    #disValue=1+min([self.getMazeDistance(gameState.getAgentPosition(self.index),self.predictInferences[i].predictPosition()) for i in self.predictInferences])
    """
    RBDomin=0.0
    tempRBValue=9999999.9
    positionRB=gameState.getAgentPosition(self.index)
    for i in self.predictinferences:
        tempPosition=self.predictInferences[i].predictPosition()
        temp=self.getMazeDistance(gameState.getAgentPosition(self.index),positionRB)
        if temp<tempRBValue:
            tempRBValue=temp
            positionRB=tempPosition
    RBDomin=self.redOrBluePos(gameState,positionRB)
    """
    #RBDomin=self.redOrBluePos(gameState,min([self.predictInferences[i].predictPosition() for i in self.predictInferences],key=lambda x:self.getMazeDistance(gameState.getAgentPosition(self.index),x)))        
    
    #opp=timeValue*RBDomin/disValue        
    opp=(1.0/(10*self.powerTimer) if self.powerTimer>0 else 1.0)*self.redOrBluePos(gameState,min([self.predictInferences[i].predictPosition() for i in self.predictInferences],key=lambda x:self.getMazeDistance(gameState.getAgentPosition(self.index),x)))*1.0/(1+min([self.getMazeDistance(gameState.getAgentPosition(self.index),self.predictInferences[i].predictPosition()) for i in self.predictInferences]))
    
    paSideValie=0.0
    parDisValue=0.0
    resultParValue=0.0
    for indexSelf in self.getTeam(gameState):
        if indexSelf!=self.index:
            parPosition=gameState.getAgentPosition(indexSelf)
            paSideValie=self.redOrBluePos(gameState,parPosition)
            parDisValue=self.getMazeDistance(parPosition,gameState.getAgentPosition(self.index))        
    resultParValue=(1.0-paSideValie)*(1.0/(1+parDisValue))
    
    faceByEn=0.0
    if self.powerTimer>0:
        faceByEn=0.0
    else: 
        if self.redOrBlue(gameState)==0:
            faceByEn=0.0
        else:
            for i in self.predictInferences:
                enemy=self.predictInferences[i].predictPosition()
                if 1.0==self.getMazeDistance(gameState.getAgentPosition(self.index),enemy):
                    faceByEn=1.0
            

    
    for i in self.getTeam(gameState):
        if i != self.index:
            parPosition=gameState.getAgentPosition(i)
    
    getCap=0.0
    if self.powerTimer>0:
        getCap=1.0
        
    oneWay=0.0
    if len(gameState.getLegalActions(self.index))<=2:
        oneWay=1.0
        
    eatFood=0.0
    tempDisPo=999999.9
    if self.redOrBlue(gameState)==0:
        eatFood=self.foodNum
        
    foodProtect=0.0
    if self.redOrBlue(gameState)==0:
        foodProtect=0.0
    else:
        selfPosition=gameState.getAgentPosition(self.index)
        for position in [(width/2,i) for i in range(1,height) if not gameState.hasWall(width/2,i)]:
            if tempDisPo>self.distancer.getDistance(selfPosition,position):
                tempDisPo=self.distancer.getDistance(selfPosition,position)
        foodProtect=tempDisPo*self.foodNum    
                
           
    stopValue=0.0
    if action==Directions.STOP:
        stopValue=1.0
    features={
        'minDisFood':resultMinFood,
     
      
        'capsules':capValue,
      
      
        'opponent':opp,
     
        'score': gameState.getScore(),
        'ally': resultParValue,
        
        'faceEnemy':faceByEn,
     
        'getCap':getCap,
        
        'oneWay':oneWay,
      
        'protect':foodProtect,
      
        'eatFood':eatFood,
      
        'stop':stopValue
        }
    weights={
           
      'minDisFood':2.0,
      
      'opponent':1.0,
      
      
      'score':800.0,
    
    
      'ally':-0.4,
      'capsules':3.0,
      
      'faceEnemy':-5000000000.0,
      
      'getCap':5000000000.0,
      'oneWay':-100,
      
      'protect':-0.01,
      'eatFood':100,
      
      'stop':-100,
      
      }
    for i in self.predictInferences:
        self.predictInferences[i].elapse(gameState)
        self.predictInferences[i].observe(gameState)
        
    return sum([weights[i]*features[i] for i in features])

  def redOrBluePos(self,gameState,position):
    width=gameState.data.layout.width
    if self.index%2==1:
     
      if position[0]<width/(2):
        return -1.0
      else:
        return 1.0
    else:
     
      if position[0]>width/2:
        return -1.0
      else:
        return 1.0

  def redOrBlue(self,gameState):
    width=gameState.data.layout.width
    position = gameState.getAgentPosition(self.index)
    if self.index%2==1:
      if position[0]<width/(2):
        return 1.0
      else:
        return 0.0
    else:
      if position[0]>width/2-1:
        return 1.0
      else:
        return 0.0


class InferenceFilter:
  def __init__(self,gameState,ourTeam,enemy):

    self.beliefs = util.Counter()
    width=gameState.data.layout.width
    height=gameState.data.layout.height
    for x in range(width):
        for y in range(height):

            if not gameState.hasWall(x,y):
                self.beliefs[(x,y)]=1.0
    self.beliefs.normalize()

    self.enemy=enemy
    self.index=ourTeam

  def predictPosition(self):
    return self.beliefs.argMax()

  def observe(self,gameState):
    enemyPosition = gameState.getAgentPosition(self.enemy)
    noisyDistance = gameState.getAgentDistances()[self.enemy]
    if enemyPosition:
        for position in self.beliefs:
            if position==enemyPosition:
                self.beliefs[position]=1.0  
            else:
                self.beliefs[position]=0.0
    else:
        for position in self.beliefs:
            distance = util.manhattanDistance(position,gameState.getAgentPosition(self.index))
            tempBelief=self.beliefs[position]
            probDis=gameState.getDistanceProb(distance,noisyDistance)
            self.beliefs[position]=tempBelief*probDis
        self.beliefs.normalize()

  def elapse(self,gameState):
    tempBeliefs = util.Counter()

    for position in self.beliefs:
        if self.beliefs[position]>0:
            nextStep={}
            x,y=position

            if not gameState.hasWall(x-1,y+0):
                nextStep[(x-1,y+0)]=1
            if not gameState.hasWall(x+0,y+0):
                nextStep[(x+0,y+0)]=1
            if not gameState.hasWall(x+1,y+0):
                nextStep[(x+1,y+0)]=1
            if not gameState.hasWall(x+0,y-1):
                nextStep[(x+0,y-1)]=1
            if not gameState.hasWall(x+0,y+1):
                nextStep[(x+0,y+1)]=1
            stepProbability=1.0/len(nextStep)
            for next in nextStep:
                tempBeliefs[next]+=stepProbability*self.beliefs[position]
    tempBeliefs.normalize()
    self.beliefs=tempBeliefs
    if self.beliefs.totalCount()<=0.0:
        width=gameState.data.layout.width
        height=gameState.data.layout.height
        for x in range(width):
            for y in range(height):
                if not gameState.hasWall(x,y):
                    self.beliefs[(x,y)]=1.0
                #self.beliefs[(x,y)]=0.0 if gameState.hasWall(i,j) else 1.0
        self.beliefs.normalize()
