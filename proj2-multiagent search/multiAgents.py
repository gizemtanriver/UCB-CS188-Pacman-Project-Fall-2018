# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        evaluation = 0
        for food in newFood.asList():
            distanceToFood = manhattanDistance(food, newPos)
            if distanceToFood < 3:
                evaluation += 2
            elif distanceToFood < 6:
                evaluation += 1
            else:
                evaluation += 0.4

        for ghostPosition in successorGameState.getGhostPositions():
            distanceToGhost = manhattanDistance(ghostPosition, newPos)
            if distanceToGhost<3: evaluation -=2
            elif newPos==ghostPosition and newScaredTimes==0: evaluation -= 1000
            else: evaluation -=0.3

        if newPos == currentGameState.getPacmanPosition(): evaluation -= 1000

        return successorGameState.getScore() + evaluation

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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_value(state, intdepth):
            if intdepth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, min_value(successor, intdepth, 1))
            return value

        def min_value(state, intdepth, agentindex):
            if intdepth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float('inf')
            for action in state.getLegalActions(agentindex):
                successor = state.generateSuccessor(agentindex, action)
                # if it is the last min agent, then the next agent is max agent. also increase depth
                if agentindex == state.getNumAgents()-1:
                    value = min(value, max_value(successor, intdepth+1))
                # if it is not the last min agent, then the next min agent in the same depth
                else:
                    value = min(value, min_value(successor, intdepth, agentindex+1))
            return value

        def minmaxDecision(gameState, intdepth):
            actionDict=util.Counter()
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                actionDict[action] = min_value(successor, intdepth, 1)
            return actionDict.argMax()

        return minmaxDecision(gameState, 0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(state, intdepth, alpha, beta):
            if intdepth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float('-inf')

            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value_new = min_value(successor, intdepth, 1, alpha, beta)
                if value_new > beta: return value_new
                value = max(value, value_new)
                alpha = max(alpha, value)
            return value

        def min_value(state, intdepth, agentindex, alpha, beta):
            if intdepth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float('inf')

            for action in state.getLegalActions(agentindex):
                successor = state.generateSuccessor(agentindex, action)
                # if it is the last min agent, then the next agent is max agent. also increase depth
                if agentindex == state.getNumAgents()-1:
                    value_new = max_value(successor, intdepth+1, alpha, beta)
                # if it is not the last min agent, then the next min agent in the same depth
                else:
                    value_new = min_value(successor, intdepth, agentindex+1, alpha, beta)
                if value_new < alpha: return value_new
                value = min(value, value_new)
                beta = min(beta, value)
            return value

        def minmaxDecision(gameState, intdepth):
            alpha = float('-inf')
            beta = float('inf')
            actionDict=util.Counter()
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                value = min_value(successor, intdepth, 1, alpha, beta)
                if value > beta: return value
                actionDict[action] = value
                alpha = max(alpha, value)
            return actionDict.argMax()

        return minmaxDecision(gameState, 0)

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

        def max_value(state, intdepth):
            if intdepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, min_value(successor, intdepth, 1))
            return value

        def min_value(state, intdepth, agentindex):
            if intdepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            totalvalue = 0
            for action in state.getLegalActions(agentindex):
                probability = 1/len(state.getLegalActions(agentindex))
                successor = state.generateSuccessor(agentindex, action)
                # if it is the last min agent, then the next agent is max agent. also increase depth
                if agentindex == state.getNumAgents() - 1:
                    value = max_value(successor, intdepth + 1)
                # if it is not the last min agent, then the next min agent in the same depth
                else:
                    value = min_value(successor, intdepth, agentindex + 1)
                totalvalue += value*probability
            return totalvalue


        def minmaxDecision(gameState, intdepth):
            actionDict = util.Counter()
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                actionDict[action] = min_value(successor, intdepth, 1)
            return actionDict.argMax()

        return minmaxDecision(gameState, 0)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Scoring based on closeness of food, capsules, ghosts and scared ghosts.
    Manhattan Distance used for distance.
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    evaluation = 0
    for food in foods.asList():
        distanceToFood = manhattanDistance(food, pos)
        if distanceToFood < 3: evaluation += 2
        elif distanceToFood < 6: evaluation += 1
        else: evaluation += 0.4

    for capsule in capsules:
        distanceToCapsule = manhattanDistance(capsule, pos)
        if distanceToCapsule < 3: evaluation += 5
        else: evaluation += 0.4

    for ghostState in ghostStates:
        if ghostState.scaredTimer: # eating a scared ghost adds points
            distanceToScaredGhost = manhattanDistance(ghostState.getPosition(), pos)
            if distanceToScaredGhost < 3: evaluation += 5
            else: evaluation +=0.4
        else: # being close to a non-scared ghost decreases points
            distanceToGhost = manhattanDistance(ghostState.getPosition(), pos)
            if distanceToGhost < 3: evaluation -= 2
            #elif pos == ghostState.getPosition() and scaredTimes == 0: evaluation -= 5
            else: evaluation -= 0.3

    return currentGameState.getScore() + evaluation

# Abbreviation
better = betterEvaluationFunction
