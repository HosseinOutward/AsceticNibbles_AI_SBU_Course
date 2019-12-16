from Src import Simulator
import random


def heuristic(ID, game):
    snake = game.players[ID]
    return 500 + snake.shekam + len(snake.body) - snake.foodScore


class AI_RBFS_S:
    currentScore=0
    def run(self, ID, game):
        self.currentScore=game.maxFoodScore
        result = self.RBFS(ID, game, 0, 100000)aa
        return result[1]

    def RBFS(self, ID, gme, fTillNow, f_limit):  # returns [success, action, f_reached]
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
        snake = game.players[ID]

        if snake.foodScore >= self.currentScore + 30:  # set to this to boost speed
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
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
        if game.nextTurn(ID, action) != 'd':
            return [game, action, 0]
        else:
            return 'd'

    # ................................................................................................


class AI_IDS:
    def run(self, ID, gme):
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
        depth=1
        while True:
            result=self.DLS(ID, game, depth)
            if result[0]:
                return result[1]

    def DLS(self, ID, game, limit):  # returns [success, action]
        if game.maxFoodScore>=500:
            return [True, -1]

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
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
        if game.nextTurn(ID, action) != 'd':
            return game
        else:
            return 'd'


class AI_A_Star:
    def run(self, ID, gme):
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
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
                if n[0].maxFoodScore>=500:
                    n[2]=q[2]+1
                    n[3]=heuristic(ID,n[0])
                    n[4]=n[2]+n[3]

                if self.lowerFExists(ID, n, openList, closedList):
                    continue
            closedList.append(q)

    def nextState(self, ID, action, gme): # [game, parent, g, h, f]
        game = Simulator.Game(1, 1, 1, 1, [])
        game.copyAllG(gme)
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
