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
        totalManhattan = 0
        error = 0
        for food in newFood.asList():
            totalManhattan += manhattanDistance(newPos,food)
        length = float((len(newFood.asList())))
        average = totalManhattan / max(length,1)
        closestFood = min([manhattanDistance(newPos, foods) for foods in currentGameState.getFood().asList()])
        ghostPos = []
        for ghosts in newGhostStates:
            manh = manhattanDistance(newPos, ghosts.getPosition())
            ghostPos.append(manh)
        closestGhost = min(ghostPos)
        if closestGhost < 2:
            error += 999999

        return (1 / float(max(average * closestFood, 0.0001))) - error        

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
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[0]
    def minimax(self, position, curdepth, player):
        best_move = None
        if position.isWin() or position.isLose() or curdepth >= self.depth:
            return best_move, self.evaluationFunction(position)
        if player == 0:
            value = -99999
        else:
            value = 99999
        for move in position.getLegalActions(player):
            next_pos = position.generateSuccessor(player,move)
            next_player = (player + 1) % position.getNumAgents()
            next_depth = curdepth
            if next_player == 0:
                next_depth += 1
            next_move, next_value = self.minimax(next_pos, next_depth, next_player)
            if player == 0 and value < next_value:
                value, best_move = next_value, move
            if player != 0 and value > next_value:
                value, best_move = next_value, move
        return best_move, value
            
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphabeta(gameState, 0, 0, -9999, 9999)[0]
    def alphabeta(self,position,curdepth,player,alpha,beta):
        best_move = None
        if position.isWin() or position.isLose() or curdepth >= self.depth:
            return best_move, self.evaluationFunction(position)
        if player == 0:
            value = -99999
        else:
            value = 99999
        for move in position.getLegalActions(player):
            next_pos = position.generateSuccessor(player,move)
            next_player = (player + 1) % position.getNumAgents()
            next_depth = curdepth
            if next_player == 0:
                next_depth += 1
            next_move, next_value = self.alphabeta(next_pos, next_depth, next_player, alpha, beta)
            if player == 0:
                if value < next_value: value, best_move = next_value, move
                if value >= beta: return best_move, value
                alpha = max(alpha, value)
            if player != 0:
                if value > next_value: value, best_move = next_value, move
                if value <= alpha: return best_move, value
                beta = min(beta,value)
        return best_move, value        

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
        return self.Expectimax(gameState, 0, 0)[0]
    def Expectimax(self, position, curdepth, player):
        best_move = None
        if position.isWin() or position.isLose() or curdepth >= self.depth:
            return best_move, self.evaluationFunction(position)
        if player == 0:
            value = -99999
        else:
            value = 99999
        legalActions = position.getLegalActions(player)
        for move in legalActions:
            next_pos = position.generateSuccessor(player,move)
            next_player = (player + 1) % position.getNumAgents()
            next_depth = curdepth
            if next_player == 0:
                next_depth += 1
            next_move, next_value = self.Expectimax(next_pos, next_depth, next_player)
            if player == 0 and value < next_value:
                value, best_move = next_value, move
            if player != 0:
                value += 1.0 / len(legalActions) * next_value
        return best_move, value        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      Things that are good for pacman: capsule, food
      Things that are bad for pacman: ghost
      Pacmen eats the closest capsule and the closest food. It stays far from the ghost. Calculating the manhattan distance between pacman and capsule, ghost and food. Returns the linear combination of manhattan distance between pacman and capsule, ghost and food.
    """
    "*** YOUR CODE HERE ***"
    closest_capsule = -9999999999
    closest_ghost = -9999999999
    closest_food = -9999999999
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    ghosts = currentGameState.getGhostStates()
    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    if len(capsules) > 0:
        closest_capsule = min([manhattanDistance(position, x) for x in capsules])
    if len(ghosts) > 0:
        closest_ghost = min([manhattanDistance(position, x.getPosition()) for x in ghosts])
    if len(foods) > 0:
        closest_food = min([manhattanDistance(position, x) for x in foods])
    return - 5*closest_food - 2*closest_capsule - 2*closest_ghost - 700*len(capsules) - 300*len(foods) + score

# Abbreviation
better = betterEvaluationFunction

