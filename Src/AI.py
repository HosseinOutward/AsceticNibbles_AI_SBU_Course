from Src import Simulator
import random


def heuristic(ID, game):
    return h1(ID,game)
    #h=game.players[ID].headPos()
    #return h2(game, h[0], h[1], game.foodGrid[h[0]][h[1]], game.players[ID].foodScore)


def h1(ID, game):
    snake=game.players[ID]

    w, h = len(game.foodGrid), len(game.foodGrid[0])
    score, moves = snake.foodScore, 0
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


class AI_Alpha_Beta:
    winScore = 500

    def run(self, ID, gme, depth):
        game = Simulator.Arena(copy=gme)
        self.winScore=game.winScore
        eval , dir= self.minimax(ID-1, ID, -1, game, depth, 10000, -10000)
        return dir

    def minimax(self, ID, mainID, dir, game, depth, alpha, beta):
        ID = (ID+1) % len(game.players)

        if depth == 0 or game.players[ID].foodScore >= self.winScore:
            return self.statEval(mainID, game), dir

        successors = []
        r = list(range(0,4))
        random.shuffle(r)
        for action in r:
            nextNode = self.nextState(ID, action, game)
            if not(nextNode is 'd'):
                successors.append(nextNode)

        if len(successors)==0:
            return -100000, dir

        if mainID==ID:
            maxEval = -100000
            for child in successors:
                eval, dir2 = self.minimax(ID+1, mainID, child[1], child[0], depth, alpha, beta)
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
                eval, dir2 = self.minimax(ID+1, mainID, child[1], child[0], depth-1, alpha, beta)
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
        #return -h2(game, h[0], h[1], game.foodGrid[h[0]][h[1]], game.players[ID].foodScore)

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
        if snake.foodScore >= self.winScore:
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


class AI_A_Star:
    winScore = 500

    def run(self, ID, gme):
        game = Simulator.Arena(copy=gme)
        self.winScore=game.winScore
        result=self.A_Star(ID, [game,0,0,0,0])
        return result[1]

    def A_Star(self, ID, node):  # returns [success, action]
        openList, closedList=[],[]
        openList.append(node)

        while len(openList)!=0:
            openList.sort(key=lambda x: x[4])
            q=openList[0]
            openList.pop(0)

            nextNodes = []
            r = list(range(0, 4))
            random.shuffle(r)
            for action in r:
                nextNode = self.nextState(ID, action, q[0])
                if nextNode != 'd':
                    nextNodes.append(nextNode)
            for n in nextNodes:
                n[1]=q

            for n in nextNodes:
                if n[0].maxFoodScore>=self.winScore:
                    n[2]=q[2]+1
                    n[3]=heuristic(ID,n[0])
                    n[4]=n[2]+n[3]

                if self.lowerFExists(ID, n, openList, closedList):
                    continue
            closedList.append(q)

    def nextState(self, ID, action, gme): # [game, parent, g, h, f]
        game = Simulator.Arena(copy=gme)
        if game.nextTurn(ID, action) != 'd':
            return [game,0,0,0,0]
        else:
            return 'd'

    def lowerFExists(self, ID, n, openList, closedList):
        for m in openList:
            if m[4] < n[4] and self.body(ID, m) == self.body(ID, n):
                return True
        for m in closedList:
            if m[4]<n[4] and self.body(ID, m)==self.body(ID, n):
                return True

    def body(self, ID, r):
        return r[0].players[ID].body
