from Src import Simulator
import random
import numpy as np
from collections import defaultdict


def heuristic(ID, game):
    return h1(ID,game)
    #h=game.players[ID].headPos()
    #return h2(game, h[0], h[1], game.foodGrid[h[0]][h[1]], game.getTeamScore(ID))


def h1(ID, game):
    snake=game.players[ID]

    w, h = len(game.foodGrid), len(game.foodGrid[0])
    score, moves = game.getTeamScore(ID), 0
    x, y, energy = snake.headPos()[0], snake.headPos()[1], snake.shekam + len(snake.body)
    begin=1
    while score < game.winScore:
        minPoint, minFood = 0, 10
        for r in range(begin, energy):
            for i in range(-r, r + 1):
                if not (x + i >= w or y + r - abs(i) >= h or x + i < 0 or y + r - abs(i) < 0):
                    if minFood > game.foodGrid[x + i][y + r - abs(i)] or game.foodGrid[x + i][y + r - abs(i)] != 0:
                        minPoint = [x + i, y + r - abs(i)]
                        minFood=game.foodGrid[x + i][y + r - abs(i)]
            for i in range(-r + 1, r):
                if not (x + i >= w or y + abs(i) - r >= h or x + i < 0 or y + abs(i) - r < 0):
                    if minFood > game.foodGrid[x + i][y + abs(i) - r] or game.foodGrid[x + i][y + abs(i) - r] != 0:
                        minPoint = [x + i, y + abs(i) - r]
                        minFood = game.foodGrid[x + i][y + abs(i) - r]

        if minPoint!=0:
            x, y = minPoint[0], minPoint[1]
            score += game.foodAddScore+game.fScoreMulti*minFood
            moves += energy
            begin=1
        else:
            begin=energy
            energy+=1
    return moves


def h2(game, x, y, energy, score, acc=5):
    w, h = len(game.foodGrid), len(game.foodGrid[0])
    moves = 0
    if score < game.winScore:
        minPoint, minFood = [0 for i in range(acc)], 10
        for r in range(1, energy):
            for i in range(-r, r + 1):
                if not (x + i >= w or y + r - abs(i) >= h or x + i < 0 or y + r - abs(i) < 0):
                    if minFood > game.foodGrid[x + i][y + r - abs(i)] or game.foodGrid[x + i][y + r - abs(i)] != 0:
                        minFood=game.foodGrid[x + i][y + r - abs(i)]
                        minPoint.append([x + i, y + r - abs(i), minFood])
                        del minPoint[0]
            for i in range(-r + 1, r):
                if not (x + i >= w or y + abs(i) - r >= h or x + i < 0 or y + abs(i) - r < 0):
                    if minFood > game.foodGrid[x + i][y + abs(i) - r] or game.foodGrid[x + i][y + abs(i) - r] != 0:
                        minFood = game.foodGrid[x + i][y + abs(i) - r]
                        minPoint.append([x + i, y + abs(i) - r, minFood])
                        del minPoint[0]

        for i in range(1, acc+1):
            mP=minPoint[-acc]
            if mP is 0:
                moves += energy + h2(game, x, y, energy+1, score, 2)
            else:
                moves += energy + h2(game, mP[0], mP[1], mP[2], score+game.foodAddScore+game.fScoreMulti*mP[2], 2)
    else:
        return 0

    return moves


class AI_Q_LEARNING:
    winScore = 500
    Q=0

    def run(self, ID, gme):
        state=gme.stateTag(ID)
        return np.argmax(self.Q[state])

    def train(self, game, count):
        self.q_learning(game, count)

    def make_epsilon_greedy_policy(self, Q, epsilon, nA):

        def policy_fn(observation):
            A = np.ones(nA, dtype=float) * epsilon / nA
            best_action = np.argmax(Q[observation])
            A[best_action] += (1.0 - epsilon)
            return A

        return policy_fn

    def q_learning(self, gme, num_episodes, discount_factor=0.9, alpha=0.9, epsilon=0.1):
        self.Q = defaultdict(lambda: np.zeros(4))

        policy = self.make_epsilon_greedy_policy(self.Q, epsilon, 4)

        for i_episode in range(num_episodes):
            env = Simulator.Arena(copy=gme)
            state, ID = env.reset()
            env.players[ID].name=True

            while True:
                action_probs = policy(state)
                action = np.random.choice(np.arange(len(action_probs)), p=action_probs)

                reward=env.getTeamScore(ID)
                #done, ID=self.nextRound(env, ID, action)
                done=env.nextTurn(ID, action)
                if done is 'd':
                    reward=-1000000
                    next_state=state
                elif done:
                    reward=100
                    reward=env.getTeamScore(ID)-reward
                    next_state=env.stateTag(ID)
                else:
                    reward=env.getTeamScore(ID)-reward
                    next_state=env.stateTag(ID)

                # TD Update
                best_next_action = np.argmax(self.Q[next_state])
                td_target = reward + discount_factor * self.Q[next_state][best_next_action]
                td_delta = td_target - self.Q[state][action]
                self.Q[state][action] += alpha * td_delta

                if done:
                    break

                state = next_state

    def nextRound(self, arena, ID, action):
        winner = False
        playerID=0
        while playerID < len(arena.players):
            if playerID == ID:
                winner = arena.nextTurn(playerID, action)
                if winner == 'd':
                    return 'd', ID
            else:
                rivalAction = int(AI_Alpha_Beta().run(playerID, arena, 20))
                winner = arena.nextTurn(playerID, rivalAction)
                if winner == 'd':
                    winner = False
                    playerID-=1
                for i, snake in enumerate(arena.players):
                    if snake.name is True: ID=i
            playerID+=1

            if winner:
                break

        if playerID == ID and winner: return True, ID
        return False, ID


class AI_Alpha_Beta:
    winScore = 500

    def run(self, ID, gme, depth):
        game = Simulator.Arena(copy=gme)
        game.players[ID].name=True
        self.winScore=game.winScore
        eval , dir= self.minimax(ID, ID, game, depth, 10000, -10000)
        return dir

    def minimax(self, curID, mainID, game, depth, alpha, beta):
        curID = curID % len(game.players)
        for i, snake in enumerate(game.players):
            if snake.name==True:
                mainID=i

        if depth == 0 or game.getTeamScore(curID) >= self.winScore:
            return self.statEval(mainID, game), -1

        successors = []
        r = list(range(0,4))
        random.shuffle(r)
        for action in r:
            nextNode = self.nextState(curID, action, game)
            if not(nextNode is 'd'):
                successors.append(nextNode)

        if len(successors)==0:
            return -100000, dir

        if game.players[curID].team == game.players[mainID].team:
            maxEval = -100000
            for child in successors:
                eval, _ = self.minimax(curID+1, mainID, child[0], depth, alpha, beta)
                maxEval = max(maxEval, eval)
                if eval == maxEval:
                    dir = child[1]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, dir
        else:
            minEval = 100000
            for child in successors:
                eval, _ = self.minimax(curID+1, mainID, child[0], depth-1, alpha, beta)
                minEval = min(minEval, eval)
                if eval == minEval:
                    dir = child[1]
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, dir

    def nextState(self, ID, action, gme):
        game = Simulator.Arena(copy=gme)
        if game.nextTurn(ID, action) != 'd':
            return [game, action]
        else:
            return 'd'

    def statEval(self, mainID, game):
        return -h1(mainID, game)
        #h=game.players[mainID].headPos()
        #return -h2(game, h[0], h[1], game.foodGrid[h[0]][h[1]], game.getTeamScore(ID))


class AI_RBFS_S:
    winScore = 500
    currentScore=0

    def run(self, ID, gme):
        game = Simulator.Arena(copy=gme)
        self.winScore=game.winScore
        self.currentScore=game.maxFoodScore
        result = self.RBFS(ID, game, 0, 100000)
        return result[1]

    def RBFS(self, ID, game, fTillNow, f_limit):  # returns [success, action, f_reached]
        snake = game.players[ID]
        if game.getTeamScore(ID) >= self.winScore:
            return [True, random.randint(0,3), f_limit]

        successors = []
        r = list(range(0,4))
        random.shuffle(r)
        for action in r:
            nextNode = self.nextState(ID, action, game)
            if nextNode != 'd':
                successors.append(nextNode)

        if len(successors)==0:
            return [False, random.randint(0,3), 100000]

        for s in successors:
            s[2] = fTillNow + 1 + heuristic(ID, s[0])

        while True:
            successors.sort(key=lambda x: x[2])
            best = successors[0]

            if best[2] > f_limit:
                return [False, best[1], best[2]]

            if len(successors)!=1:
                altF = successors[1][2]
            else:
                altF = best[2]

            result = self.RBFS(ID, best[0], fTillNow+1, min(f_limit, altF))
            best[2] = result[2]

            if result[0]:
                return [True, best[1], best[2]]

    def nextState(self, ID, action, gme):
        game = Simulator.Arena(copy=gme)
        if game.nextTurn(ID, action) != 'd':
            return [game, action, 0]
        else:
            return 'd'

    # ................................................................................................


class AI_IDS:
    winScore = 500

    def run(self, ID, gme):
        game = Simulator.Arena(copy=gme)
        self.winScore=game.winScore
        depth=1
        while True:
            result=self.DLS(ID, game, depth)
            if result[0]:
                return result[1]
            depth+=game.players[ID].shekam + len(game.players[ID].body)

    def DLS(self, ID, game, limit):  # returns [success, action]
        if game.maxFoodScore >= self.winScore:
            return [True, -1]
        elif limit == 0:
            return [False, -1]

        r = list(range(0,4))
        random.shuffle(r)
        for action in r:
            childGame = self.nextState(ID, action, game)
            if childGame != 'd':
                result = self.DLS(ID, childGame, limit-1)
                if result[0]:
                    return[True, action]
        return[False, -1]

    def nextState(self, ID, action, gme):
        game = Simulator.Arena(copy=gme)
        if game.nextTurn(ID, action) != 'd':
            return game
        else:
            return 'd'
    # ................................................................................................
