# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    #define a dictionary to store values in iterations for each state
    self.valueRecord = {}
    for state in mdp.getStates():
      self.valueRecord[state] = []
    
    for i in range(0, self.iterations + 1):
      for state in mdp.getStates():
        if i == 0 or mdp.isTerminal(state):
          self.valueRecord[state].append(0)
          continue
        actions = mdp.getPossibleActions(state)
        #store the current reward as value and return
        if 'exit' in actions:
          self.valueRecord[state].append(mdp.getReward(state, 'exit', mdp.getTransitionStatesAndProbs(state, 'exit')[0][0]))
          continue
        max = float("-inf")
        #find the action that maximize the value 
        for action in actions:
          summax = 0
          for (s,p) in mdp.getTransitionStatesAndProbs(state, action):
            summax += p * (mdp.getReward(state, action, s) + self.discount * self.valueRecord[s][i-1])
          if summax > max:
            max = summax
        self.valueRecord[state].append(max)
    #store the final value we get from iteration into values
    for k, v in self.valueRecord.items():
      self.values[k] = v[iterations]
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    sumQ = 0
    
    for (s, p) in self.getTransitionStatesAndProbs(state, action):
      sumQ += p * (self.mdp.getReward(state, action, s) + self.discount * self.values[s])
    
    return sumQ

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    bestAction = None
    actions = self.mdp.getPossibleActions(state)
    
    if self.mdp.isTerminal(state):
      return bestAction
    if 'exit' in actions:
      return 'exit'
    
    max = float("-inf")
    for action in actions:
      summax = 0
      for (s,p) in self.mdp.getTransitionStatesAndProbs(state, action):
        summax += p * (self.mdp.getReward(state, action, s) + self.discount * self.valueRecord[s][self.iterations - 1])
        if summax > max:
          max = summax
          bestAction = action
          
    return bestAction

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
