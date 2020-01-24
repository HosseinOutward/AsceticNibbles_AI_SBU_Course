import pygame
from string import ascii_lowercase as alphabeta

class Graphics:
    pixelWidth, pixelHeight, page, cubeSize = 0, 0, 0, 0

    def __init__(self, w, h, cubeSize, game):
        self.cubeSize = cubeSize
        self.pixelWidth, self.pixelHeight = w * self.cubeSize+w-1, h * self.cubeSize+h-1
        self.page = pygame.display.set_mode((self.pixelWidth+ 6*self.cubeSize, self.pixelHeight+ 2*self.cubeSize))
        self.redrawPage(game)

    def redrawPage(self, game):
        self.page.fill((0,0,0))
        self.drawFood(game)
        self.drawSnake(game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def drawFood(self, game):
        for i in range(len(game.foodGrid)):
            for j in range(len(game.foodGrid[i])):
                color = game.foodGrid[i][j]*255//9
                self.colorCube(i, j, (255-color, 255, 255-color))

    def drawSnake(self, game):
        for snake in game.players:
            for part in snake.body:
                self.colorCube(part[0], part[1], snake.color)
            self.markHead(snake.body[-1][0], snake.body[-1][1])

    def drawText(self, text, color, delay):
        pygame.draw.rect(self.page, (0,0,0), (0,self.pixelHeight , self.pixelWidth, 2*self.cubeSize))
        pygame.font.init()
        font = pygame.font.SysFont('arial', self.cubeSize)
        text_surface = font.render(text, True, color)
        self.page.blit(text_surface, (self.cubeSize//3, self.pixelHeight+self.cubeSize//3))
        pygame.display.update()
        pygame.time.delay(delay)

    def drawScores(self, game):
        for i in range(game.numT):
            pygame.draw.rect(self.page, (0,0,0), (0,self.pixelHeight , self.pixelWidth, 2*self.cubeSize))
            pygame.font.init()
            font = pygame.font.SysFont('arial', self.cubeSize)

            color=game.players[i].color
            text = "Team " + alphabeta[i].upper() + ": " + str(game.getTeamScore(i))
            text_surface = font.render(text, True, color)

            x=len(game.foodGrid)*(self.cubeSize+1)+self.cubeSize//3
            y=i*self.cubeSize+i*self.cubeSize//3
            self.page.blit(text_surface, (x, y))

            pygame.display.update()


    def colorCube(self, i, j, color):
        pygame.draw.rect(self.page, color, (self.pixelPos(i), self.pixelPos(j), self.cubeSize, self.cubeSize))

    def markHead(self, i, j):
        circlePos = (self.pixelPos(i) + 2 * self.cubeSize // 7, self.pixelPos(j) + 2*self.cubeSize // 5)
        pygame.draw.circle(self.page, (0, 0, 0), circlePos, self.cubeSize // 10)
        circlePos = (self.pixelPos(i) + 5 * self.cubeSize // 7, self.pixelPos(j) + 2*self.cubeSize // 5)
        pygame.draw.circle(self.page, (0, 0, 0), circlePos, self.cubeSize // 10)

    def pixelPos(self, i):
        return i * self.cubeSize + i

    def getAction(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        return 1
                    if event.key == pygame.K_RIGHT:
                        return 3
                    if event.key == pygame.K_DOWN:
                        return 0
                    if event.key == pygame.K_UP:
                        return 2
