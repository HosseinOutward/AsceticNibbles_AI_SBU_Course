import random


class Arena:
    players, foodAddScore, fScoreMulti, maxFoodScore, foodGrid, consume, winScore, turnCost, numT = [], 0, 0, 0, 0, 0, 0, 0, 0

    def __init__(self, *args, copy=None):
        if copy is None:
            self.firstInit(*args)
        elif copy is 'f':
            self.loadFromFile()
        else:
            self.copyInit(copy)

    def firstInit(self, width, height, consumeMode, trnCost, fScoreAdd, fScoMul, winScr, numT,names, types):
        self.consume, self.turnCost, self.foodAddScore, self.fScoreMulti, self.winScore, self.numT = consumeMode, trnCost, fScoreAdd, fScoMul, winScr, numT
        self.foodGrid = [[random.randint(1, 9) for j in range(height)] for i in range(width)]
        for i in range(len(names)):
            self.players.append(Snake(names[i], types[i], width, height, i + 1, self.players, i%numT))
        for ID in range(len(self.players)):
            self.eat(ID)

    def copyInit(self, gameToCopy):
        self.players = []
        for snake in gameToCopy.players:
            self.players.append(Snake(copy=snake))
        self.foodGrid = [[a for a in collumn] for collumn in gameToCopy.foodGrid]
        self.foodAddScore = gameToCopy.foodAddScore
        self.winScore = gameToCopy.winScore
        self.turnCost = gameToCopy.turnCost
        self.maxFoodScore = gameToCopy.maxFoodScore
        self.consume = gameToCopy.consume
        self.numT = gameToCopy.numT
        self.fScoreMulti = gameToCopy.fScoreMulti

    def loadFromFile(self):
        load

    def nextTurn(self, ID, action):
        snake = self.players[ID]
        snake.move(int(action))
        if self.impact(snake.headPos()):
            self.kill(snake)
            return 'd'
        else:
            self.eat(ID)
            if snake.currentDir != action:
                snake.foodScore -= self.turnCost
            snake.currentDir = action
        if self.maxFoodScore >= self.winScore:
            return True
        return False

    def eat(self, ID):
        snake=self.players[ID]
        if snake.shekam + len(snake.body) == 1:
            snake.foodScore += 1 + self.fScoreMulti * self.foodGrid[snake.headPos()[0]][snake.headPos()[1]]
            snake.shekam += self.foodGrid[snake.headPos()[0]][snake.headPos()[1]]
            if self.getTeamScore(ID) > self.maxFoodScore:
                self.maxFoodScore = self.getTeamScore(ID)
            if self.consume:
                self.foodGrid[snake.headPos()[0]][snake.headPos()[1]] = 0

    def getTeamScore(self, ID):
        snake=self.players[ID]
        score=0
        for Othersnake in self.players:
            if Othersnake.team==snake.team:
                score+=Othersnake.foodScore
        return score

    def impact(self, pos):
        width, height = len(self.foodGrid), len(self.foodGrid[0])
        if pos[0] == width or pos[1] == height or pos[0] == -1 or pos[1] == -1:
            return True

        i = 0
        for OtherSnake in self.players:
            for part in OtherSnake.body:
                if pos[0] == part[0] and pos[1] == part[1]:
                    i += 1

        if i > 1:
            return True

        return False

    def kill(self, snake):
        self.players.remove(snake)


# ...
class Snake:
    shekam, team, body, color, name, foodScore, realScore, type, currentDir = 0, 0, 0, 0, 0, 0, 0, 0, -1

    def __init__(self, *args, copy=None):
        if copy is None:
            self.firstInit(*args)
        else:
            self.copyInit(copy)

    def firstInit(self, name, type, width, height, colorNum, playersList, team):
        self.name, self.color, self.type, self.team = name, self.randColor(colorNum), type, team
        diffrent = True
        while diffrent:
            diffrent, tempBody = False, [(random.randint(0, width - 1), random.randint(0, height - 1))]
            for snake in playersList:
                if tempBody is snake.body:
                    diffrent = True
        self.body = tempBody

    def copyInit(self, snakeToCopy):
        self.shekam = snakeToCopy.shekam
        self.body = [[a for a in part] for part in snakeToCopy.body]
        self.color = snakeToCopy.color
        self.name = snakeToCopy.name
        self.foodScore = snakeToCopy.foodScore
        self.realScore = snakeToCopy.realScore
        self.type = snakeToCopy.type
        self.team = snakeToCopy.team

    def move(self, dir):  # down=0, left=1, up=2, right=3
        if dir == 0:
            self.body.append((self.headPos()[0], self.headPos()[1] + 1))
        elif dir == 1:
            self.body.append((self.headPos()[0] - 1, self.headPos()[1]))
        elif dir == 2:
            self.body.append((self.headPos()[0], self.headPos()[1] - 1))
        elif dir == 3:
            self.body.append((self.headPos()[0] + 1, self.headPos()[1]))
        elif dir== -1:
            return self.move(random.randint(0, 3))

        if self.shekam == 0:
            del self.body[0]
            if len(self.body) != 1:
                del self.body[0]
        else:
            self.shekam -= 1

        self.realScore += 1

    def headPos(self):
        return self.body[-1]

    def randColor(self, n):
        ret = 0
        r = int(random.random() * 220) + 30
        g = int(random.random() * 150)
        b = int(random.random() * 200) + 30
        step = 256 / n
        for i in range(n):
            r += step
            g += step
            b += step
            r = int(r) % 256
            g = int(g) % 256
            b = int(b) % 256
            ret = (r, g, b)
        return ret

