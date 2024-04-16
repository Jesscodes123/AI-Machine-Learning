
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
        f0 = successorGameState.getScore()

        # ------------------------------------
        # number of remaining food dots: the smaller the better
        newFoodList = newFood.asList()

        f1 = 1 / max(len(newFoodList), 1)

        # ------------------------------------
        # distance to the closest food dot: the smaller the better
        closestFoodDistance = float("inf")
        for foodPosition in newFoodList:
        	distance = util.manhattanDistance(newPos, foodPosition)
        	if closestFoodDistance > distance:
        		closestFoodDistance = distance
        f4 = 1 / max(closestFoodDistance, 1)


        # ------------------------------------
        # distance to the closest ghost: the larger the better
        # E, MH, MAZE
        # total distance to all ghosts: the larger the better

        totalDistance = 0
        closestDistance = float("inf")
        for ghostState in newGhostStates:
        	ghostPosition = ghostState.getPosition() # x, y
        	distance = util.manhattanDistance(newPos, ghostPosition)
        	totalDistance += distance
        	if closestDistance > distance:
        		closestDistance = distance

        f2 = - 1 / max(closestDistance, 1)
        f3 = - 1 / max(totalDistance, 1)
        # f3 = max(totalDistance, 1)
        
        # return f1 + f2 + f3
        # return f0 + f1 + f2 + f3
        # return f1 + f2 + f3 + f4
        return f0 + f1 + f2 + f3 + f4
        # return f0 + f2 + f3 + f4



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
        # util.raiseNotDefined()
        #=================================== Verstion 0: incorrect!
        # def value(gameState, agentIndex):
        #     if gameState.isLose() or gameState.isWin():
        #         return self.evaluationFunction(gameState), None
  
        #     if agentIndex == 0:
        #         nextAgentIndex = 1
        #         v = float("-inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex)
        #             if v < nextV:
        #                 v = nextV
        #                 bestAction = action
        #         return v, bestAction
        #     else:
        #         nextAgentIndex =  agentIndex + 1
        #         # 3 = 1 + 2
        #         if gameState.getNumAgents() == nextAgentIndex:
        #             nextAgentIndex = 0

        #         v = float("inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex)
        #             if v > nextV:
        #                 v = nextV
        #                 bestAction = action
        #         return v, bestAction

        # v, action = value(gameState, 0)
        # return action
        def value(gameState, agentIndex, depth):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState), None
  
            if agentIndex == 0:
                nextAgentIndex = 1

                bestValue = float("-inf")
                bestAction = None
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    nextV, _ = value(nextGameState, nextAgentIndex, depth)
                    if bestValue < nextV:
                        bestValue = nextV
                        bestAction = action
                return bestValue, bestAction
            else:
                nextAgentIndex =  agentIndex + 1
                # 3 = 1 + 2
                if gameState.getNumAgents() == nextAgentIndex:
                    nextAgentIndex = 0
                    depth = depth + 1

                bestValue = float("inf")
                bestAction = None
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    nextV, _ = value(nextGameState, nextAgentIndex, depth)
                    if bestValue > nextV:
                        bestValue = nextV
                        bestAction = action
                return bestValue, bestAction

        bestValue, action = value(gameState, 0, 0)
        return action
        #=================================== Verstion 1
        # def value(gameState, agentIndex, depth):
        #     if gameState.isLose() or gameState.isWin() or depth == self.depth:
        #         return self.evaluationFunction(gameState), None
  
        #     if agentIndex == 0:
        #         nextAgentIndex = 1
        #         v = float("-inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex, depth)
        #             if v < nextV:
        #                 v = nextV
        #                 bestAction = action
        #         return v, bestAction
        #     else:
        #         nextAgentIndex =  agentIndex + 1
        #         # 3 = 1 + 2
        #         if gameState.getNumAgents() == nextAgentIndex:
        #             nextAgentIndex = 0
        #             depth += 1

        #         v = float("inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex, depth)
        #             if v > nextV:
        #                 v = nextV
        #                 bestAction = action
        #         return v, bestAction

        # v, action = value(gameState, 0, 0)
        # return action

        #=================================== Verstion 2
        # def value(gameState, agentIndex, depth):
        #     if gameState.isLose() or gameState.isWin() or depth == self.depth:
        #         return self.evaluationFunction(gameState), None
            
        #     # -------------------- max agent
        #     if agentIndex == 0: 
        #         nextAgentIndex = 1
        #         bestValue = float("-inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex, depth)
        #             if bestValue < nextV: # bestValue is the max value
        #                 bestValue = nextV
        #                 bestAction = action
        #         return bestValue, bestAction
        #     # -------------------- min agent
        #     else:
        #         nextAgentIndex =  agentIndex + 1
        #         # 3 = 1 + 2
        #         if gameState.getNumAgents() == nextAgentIndex:
        #             nextAgentIndex = 0
        #             depth = depth + 1

        #         bestValue = float("inf")
        #         bestAction = None
        #         for action in gameState.getLegalActions(agentIndex):
        #             nextGameState = gameState.generateSuccessor(agentIndex, action)
        #             nextV, _ = value(nextGameState, nextAgentIndex, depth)
        #             if bestValue > nextV:
        #                 bestValue = nextV
        #                 bestAction = action
        #         return bestValue, bestAction

        # _, action = value(gameState, 0, 0)
        # return action








class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # "*** YOUR CODE HERE ***"
        

        def value(gameState, agentIndex, depth, alpha, beta):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState), None
  
            if agentIndex == 0:
                nextAgentIndex = 1

                bestValue = float("-inf")
                bestAction = None
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    nextV, _ = value(nextGameState, nextAgentIndex, depth, alpha, beta)
                    if bestValue < nextV:
                        bestValue = nextV
                        bestAction = action
                    if bestValue > beta:
                        return bestValue, bestAction
                    alpha = max(alpha, bestValue)
                return bestValue, bestAction
            else:
                nextAgentIndex =  agentIndex + 1
                # 3 = 1 + 2
                if gameState.getNumAgents() == nextAgentIndex:
                    nextAgentIndex = 0
                    depth = depth + 1

                bestValue = float("inf")
                bestAction = None
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    nextV, _= value(nextGameState, nextAgentIndex, depth, alpha, beta)
                    if bestValue > nextV:
                        bestValue = nextV
                        bestAction = action
                    if bestValue < alpha:
                        return bestValue, bestAction
                    beta = min(beta, bestValue)
                return bestValue, bestAction

        alpha = float("-inf")
        beta = float("inf")
        _, action = value(gameState, 0, 0, alpha, beta)
        return action

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
        # util.raiseNotDefined()
        def value(gameState, agentIndex, depth):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState), None
  
            if agentIndex == 0:
                nextAgentIndex = 1

                bestValue = float("-inf")
                bestAction = None
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    nextV, _ = value(nextGameState, nextAgentIndex, depth)
                    if bestValue < nextV:
                        bestValue = nextV
                        bestAction = action
                return bestValue, bestAction
            else:
                nextAgentIndex =  agentIndex + 1
                # 3 = 1 + 2
                if gameState.getNumAgents() == nextAgentIndex:
                    nextAgentIndex = 0
                    depth = depth + 1

                averageValue = 0
                for action in gameState.getLegalActions(agentIndex):
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    p = 1.0 / len(gameState.getLegalActions(agentIndex))
                    nextV, _ = value(nextGameState, nextAgentIndex, depth)
                    averageValue += p * nextV
                return averageValue, None

        bestValue, action = value(gameState, 0, 0)
        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    f0 = currentGameState.getScore()

    # ------------------------------------
    # number of remaining food dots: the smaller the better
    newFoodList = newFood.asList()

    f1 = 1 / max(len(newFoodList), 1)

    # ------------------------------------
    # distance to the closest food dot: the smaller the better
    closestFoodDistance = float("inf")
    for foodPosition in newFoodList:
        distance = util.manhattanDistance(newPos, foodPosition)
        if closestFoodDistance > distance:
            closestFoodDistance = distance
    f4 = 1 / max(closestFoodDistance, 1)

    # ------------------------------------
    # distance to the closest ghost: the larger the better
    # E, MH, MAZE
    # total distance to all ghosts: the larger the better
    totalDistance = 0
    closestDistance = float("inf")
    for ghostState in newGhostStates:
        ghostPosition = ghostState.getPosition() # x, y
        distance = util.manhattanDistance(newPos, ghostPosition)
        totalDistance += distance
        if closestDistance > distance:
            closestDistance = distance

    f2 = - 1 / max(closestDistance, 1)
    f3 = - 1 / max(totalDistance, 1)
    # f3 = max(totalDistance, 1)
    
    # -----------------------------------
    # consider the capsules
    newCapsules = currentGameState.getCapsules()

    f5 = 1/max(len(newCapsules), 1)

    # return f1 + f2 + f3
    # return f0 + f1 + f2 + f3
    # return f1 + f2 + f3 + f4
    return f0 + f1 + f2 + f3 + f4 + f5
    # return f0 + f2 + f3 + f4











# Abbreviation
better = betterEvaluationFunction
