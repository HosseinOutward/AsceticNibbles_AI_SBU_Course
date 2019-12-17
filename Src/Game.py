from Src import GUI, Simulator, AI


def askForAction(x, playerID, arena, gui):
    if x == "IDS":
        return AI.AI_IDS().run(playerID, arena)
    if x == "RBFS":
        return AI.AI_RBFS_S().run(playerID, arena)
    #if x == "A_STAR":
    #    return AI.AI_A_Star().run(playerID, arena)
    if x == "HUMAN":
        return gui.getAction()


def getInit():
    fScoreAdd =  int(input("fScore Add "))
    fScoreMulti = int(input("fScore Multi "))
    width = int(input("Width "))
    height = int(input("Height "))
    consumeMode = input("Consume mode (B or A) ")
    if consumeMode != "B" or "b":
        consumeMode = False
    else:
        consumeMode = True

    numP = int(input("number of players "))
    PlayerNames, PlayersType =[], []
    for i in range(numP):
        PlayerNames.append(str(input("name ")))
        PlayersType.append(str(input("whats players Type of" + PlayerNames[i] + "(type EXACTLY: IDS, RBFS or Human )")).upper())

    winScore = int(input("Score to Win "))
    trnCost = float(input("Turning Penalty "))
    cubeSize = int(input("Window Size (ex. 30 for FHD)"))

    arena = Simulator.Arena(width, height, consumeMode, trnCost, fScoreAdd, fScoreMulti, winScore, PlayerNames, PlayersType)
    gui = GUI.Graphics(width, height, cubeSize, arena)
    return arena, gui
# ..................................................................


def main():
    #arena = Simulator.Arena(10, 5, True, 0.5, 3, 2, 20, ["alex", "john"], ["RBFS", "IDS"])
    #gui = GUI.Graphics(10, 5, 30, arena)
    arena, gui = getInit()

    winner = False
    while not(winner or len(arena.players)==0):
        playerID = 0
        for snake in arena.players:
            gui.drawText("its " + str(snake.name) + "'s turn", snake.color, 10)
            action = int(askForAction(snake.type, playerID, arena, gui))
            winner = arena.nextTurn(playerID, action)
            if winner == 'd':
                winner = False
            gui.redrawPage(arena)
            gui.drawText("your score is " + str(snake.foodScore), snake.color, 500)
            if winner:
                break
            playerID += 1

    if winner:
        gui.drawText("Winner, Winner, Chicken Dinner. ", (255,215,0), 1000)
        gui.drawText(str(arena.players[playerID].name) + " won.", (255,215,0), 1000)
    else:
        gui.drawText("GAME OVER", (255,255,255), 1000)
        for snake in arena.players:
            gui.drawText(str(snake.realScore) + " moves by " + str(snake.name), arena.players[playerID].color, 1000)
# ..................................................................


main()
