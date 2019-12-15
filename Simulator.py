import copy
import numpy.random as npR
import random

class Game:
    players, fScoreMulti, maxFoodScore, foodGrid, consume = [], 0, 0, 0, 0

    def __init__(self, width, height, mode, fScoMul, names):
        self.consume, self.fScoreMulti, self.foodGrid = mode, fScoMul, npR.randint(9, size=(width, height))+1
        # need balancing for duo
        i = 1
        for name in names:
            self.players.append(Snake(name, width, height, i, self.players))
            i+=1
        for snake in self.players:
            self.eat(snake)

    def nextTurn(self, ID, action):
        snake = self.players[ID]
        snake.move(int(action))
        if self.impact(snake.headPos()):
            self.kill(snake)
            return 'd'
        else:
            self.eat(snake)
        if self.maxFoodScore >= 500:
            return True
        return False

    def eat(self, snake):
        if snake.shekam + len(snake.body) == 1:
            snake.foodScore += 1 + self.fScoreMulti * self.foodGrid[snake.headPos()[0]][snake.headPos()[1]]
            snake.shekam += self.foodGrid[snake.headPos()[0]][snake.headPos()[1]]
            if snake.foodScore > self.maxFoodScore:
                self.maxFoodScore = snake.foodScore
            if self.consume:
                self.foodGrid[snake.headPos()[0]][snake.headPos()[1]] = 0

    def impact(self, pos):
        width, height = len(self.foodGrid), len(self.foodGrid[0])
        if pos[0] == width or pos[1] == height or pos[0] == -1 or pos[1] == -1:
            return True

        i=0
        for OtherSnake in self.players:
            for part in OtherSnake.body:
                if pos[0] == part[0] and pos[1] == part[1]:
                    i += 1

        if i > 1:
            return True

        return False

    def kill(self, snake):
        self.players.remove(snake)

    def copyAllG(self, gme):
        temp = []
        for snake in gme.players:
            temp.append(Snake(1,1,1,1,[]))
            temp[-1].copyAllS(snake)
        self.players = temp
        self.foodGrid = copy.deepcopy(gme.foodGrid)
        self.maxFoodScore = copy.deepcopy(gme.maxFoodScore)
        self.consume = copy.deepcopy(gme.consume)
        self.fScoreMulti = copy.deepcopy(gme.fScoreMulti)

# ...
class Snake:
    shekam, body, color, name, foodScore, realScore = 0, 0, 0, 0, 0, 0

    def __init__(self, name, width, height, colorNum, playersList):
        self.name, self.color = name, self.randColor(colorNum)
        same = True
        while same:
            same, tempBody = False, [(random.randint(0, width-1), random.randint(0, height-1))]
            for snake in playersList:
                if tempBody is snake.body:
                    same = True
        self.body = tempBody

    def move(self, dir):  # down=0, left=1, up=2, right=3
        if dir == 0:
            self.body.append((self.headPos()[0], self.headPos()[1]+1))
        elif dir == 1:
            self.body.append((self.headPos()[0]-1, self.headPos()[1]))
        elif dir == 2:
            self.body.append((self.headPos()[0], self.headPos()[1]-1))
        elif dir == 3:
            self.body.append((self.headPos()[0]+1, self.headPos()[1]))

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
        r = int(random.random() * 220)+30
        g = int(random.random() * 150)
        b = int(random.random() * 200)+30
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

    def copyAllS(self, snake):
        self.shekam = copy.deepcopy(snake.shekam)
        self.body = copy.deepcopy(snake.body)
        self.color = copy.deepcopy(snake.color)
        self.name = copy.deepcopy(snake.name)
        self.foodScore = copy.deepcopy(snake.foodScore)
        self.realScore = copy.deepcopy(snake.realScore)
