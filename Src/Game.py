from Src import GUI, Simulator, AI
import dill

def askForAction(x, playerID, arena, gui,ai):
    if x == "IDS":
        return AI.AI_IDS().run(playerID, arena)
    if x == "RBFS":
        return AI.AI_RBFS_S().run(playerID, arena)
    if x == "MINMAX":
        return AI.AI_Alpha_Beta().run(playerID, arena, 15)
    if x == "Q-LEARNING":
        return ai.run(playerID, arena)
    #if x == "A_STAR":
    #    return AI.AI_A_Star().run(playerID, arena)

    return gui.getAction()


def getInit(a):
    ai=0
    if a == 'Y':
        arena = dill.load(open("SavedStates/arena.pickle", "rb"))
        a=arena.foodGrid
        gui = GUI.Graphics(len(a), len(a[0]), 30, arena)
        ai = dill.load(open("SavedStates/Q_AI.pickle", "rb"))
            #bug below, should be fixed soon...
        g = Simulator.Arena(20, 10, True, 1, 5, 15, 400, 3, ["Q_agent1", "Q_agent2", "MMb", "MMc", "MMd", "MMe"], ["Q-LEARNING", "Q-LEARNING", "MINMAX", "MINMAX", "MINMAX", "MINMAX"], True)
        arena.players=[Simulator.Snake(copy=a) for a in g.players]

    elif a == 'N':
        fScoreAdd = int(input("fScore Add "))
        fScoreMulti = int(input("fScore Multi "))
        width = int(input("Width "))
        height = int(input("Height "))

        consumeMode = input("Consume mode (B or A) ")
        if consumeMode != "B" or "b":
            consumeMode = False
        else:
            consumeMode = True

        stochastic = input("stochastic (Y or N) ")
        if stochastic != "Y" or "y":
            stochastic = False
        else:
            stochastic = True

        numT = int(input("number of teams (one for solo) "))
        numP = int(input("number of players per team"))

        PlayerNames, PlayersType = [], []
        for i in range(numP*numT):
            PlayerNames.append(str(input("name of player from team " + (i%numT+1) + ": ")))
            PlayersType.append(str(input("whats Type of" + PlayerNames[i] + "(type EXACTLY: IDS, MinMax, RBFS, Q-learning (will load from file) or Human )")).upper())
            if PlayersType[-1] is "Q-LEARNING":
                ai = dill.load(open("Q_AI.pickle", "rb"))

        winScore = int(input("Score to Win "))
        trnCost = float(input("Turning Penalty "))
        cubeSize = int(input("Window Size (ex. 30 for FHD)"))

        arena = Simulator.Arena(width, height, consumeMode, trnCost, fScoreAdd, fScoreMulti, winScore, numT, PlayerNames, PlayersType, stochastic)
        gui = GUI.Graphics(width, height, cubeSize, arena)

        if str(input("save this World? Y/N")).upper() is 'Y': dill.dump(arena, file = open("arena.pickle", "wb"))

    else:
        arena = Simulator.Arena(10, 5, True, 1, 5, 15, 400, 2, ["Q_agent", "MMa"], ["Q-LEARNING", "MINMAX"], True)
        gui = GUI.Graphics(10, 5, 30, arena)
        ai=AI.AI_Q_LEARNING()
        ai.train(arena, 10000)
        #dill.dump(arena, file=open("SavedStates/arena.pickle", "wb"))
        #dill.dump(ai, file=open("SavedStates/Q_AI.pickle", "wb"))

    return arena, gui, ai
# ..................................................................


def main():
    #arena, gui = getInit(str(input("Load from file? (y/n) ")))
    arena, gui, ai = getInit(str(input("load? Y/N ")).upper())


    winner = False
    while not(winner or len(arena.players)==0):
        playerID = 0
        for snake in arena.players:
            gui.drawText("its " + str(snake.name) + " of team " + str(snake.team) + "'s turn", snake.color, 25)
            action = int(askForAction(snake.type, playerID, arena, gui,ai))
            winner = arena.nextTurn(playerID, action)
            gui.redrawPage(arena)
            if winner == 'd':
                winner = False
            else:
                gui.drawText(str(snake.name) + " of team " + str(snake.team) + " score is " + str(arena.getTeamScore(playerID)), snake.color, 2000)
            if winner:
                break
            playerID += 1

    if winner:
        gui.drawText("Winner, Winner, Chicken Dinner. ", (255,215,0), 3000)
        gui.drawText(str(arena.players[playerID].name) + " won.", arena.players[playerID].color, 5000)
    else:
        gui.drawText("GAME OVER", (255,255,255), 1000)
        for snake in arena.players:
            gui.drawText(str(snake.realScore) + " moves by " + str(snake.name), arena.players[playerID].color, 10000)
# ..................................................................


main()