from Src import GUI, Simulator, AI


class IO:
    def __init__(self):
        a=0

    def send(self, game):
        return game

    def get(self):
        return input()


def getInit():
    fScoreMulti = int(input("fScoreMulti "))
    width = int(input("width "))
    height = int(input("height "))
    mode = input("mode ")
    if mode != "B" or "b":
        mode = False
    else:
        mode = True
    numP = int(input("number of players "))
    PlayerNames=[]
    for i in range(numP):
        PlayerNames.append(str(input("name ")))
    playersType = str(input("players Type (type EXACTLY: IDS, RBFS or Human )")).upper()
    cubeSize = int(input("Window Size "))
    return width, height, mode, fScoreMulti, PlayerNames, playersType, cubeSize


def askForAction(x, playerID, arena, gui):
    if x == "IDS":
        return AI.AI_IDS().run(playerID, arena)
    if x == "RBFS":
        print("this works, but it takes some time to act")
        return AI.AI_RBFS_S().run(playerID, arena)
    #if x == "A_STAR":
    #    return AI.AI_A_Star().run(playerID, arena)
    if x == "HUMAN":
        return gui.getAction()
# ..................................................................


def main():
    width, height, mode, fScoreMulti, PlayerNames, playersType, cubeSize = getInit()

    arena = Simulator.Game(width, height, mode, fScoreMulti, PlayerNames)

    gui = GUI.Graphics(width, height, cubeSize, arena)

    winner = False
    while not(winner or len(arena.players)==0):
        playerID = 0
        for snake in arena.players:
            gui.drawText("its " + str(snake.name) + "'s turn", snake.color, 10)  # io
            action = int(askForAction(playersType, playerID, arena, gui))  # io
            winner = arena.nextTurn(playerID, action)
            if winner == 'd':
                winner = False
            gui.redrawPage(arena)  # io
            if winner:
                break
            playerID += 1

    if winner:
        gui.drawText("Winner, Winner, Chicken Dinner. ", (255,215,0), 500)  # io
        gui.drawText(str(arena.players[playerID].name) + " won.", (255,215,0), 500)  # io
    else:
        gui.drawText("GAME OVER", (255,255,255), 500)  # io
        for snake in arena.players:
            gui.drawText(str(snake.realScore) + " moves by " + str(snake.name), arena.players[playerID].color, 500)  # io
# ..................................................................


main()
