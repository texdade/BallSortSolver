import json, sys, copy

blockedSituations = set()

def checkMoves(ballData, current):
    #return empty list if the vial is empty
    if(len(ballData[current]) == 0):
        return []

    #get the color of the ball when want to move
    color = ballData[current][-1]
    moves = list()

    #check all moves
    i = 0 #index of vial
    for vial in ballData:
        #skip the vial that contains the ball we have to move
        if(current == i):
            i+=1
            continue

        if len(vial) == 0:
            #put the empty vial move at the back, so more meaningful moves can be done before
            if(not sameColor(ballData[current])):
                moves.append((current, i))
        #if there is a ball of the same color and the vial isn't full
        elif color == vial[-1] and len(vial) < 4:
            #check if the move isn't blocked
            moves.insert(0, (current, i))
        
        i+=1

    return moves

def sameColor(vial):
    if(len(set(vial)) == 1):
        return True

def checkWinCon(ballData):
    for vial in ballData:
        #vials must be either empty or have only balls of the same color
        if(vial != []):
            if(len(vial) == 4):
                if(not sameColor(vial)):
                    return False
            else:
                return False
    
    return True

def solve(ballData, current):
    print(ballData)

    if(current == len(ballData)):
        current = 0

    if(checkWinCon(ballData)):
        print(ballData)
        return True

    #check possible moves
    moves = checkMoves(ballData, current)

    #if we don't have moves, check next vial
    if(moves == []):
        return solve(ballData, current+1)

    for move in moves:
        ballDataTemp = copy.deepcopy(ballData)
        ball = ballDataTemp[move[0]].pop()
        ballDataTemp[move[1]].append(ball)

        if(makeHash(ballDataTemp) not in blockedSituations):
            blockedSituations.add(makeHash(ballDataTemp))
            if(solve(ballDataTemp, current)):
                return True

def makeHash(ballData):
    hashedValue = str()

    for vial in ballData:
        if(len(vial) > 0):
            for ball in vial:
                hashedValue += str(ball)
        else:
            hashedValue += str(0)

    print(hashedValue)

    return int(hashedValue)

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("ERROR: must specify input JSON file!")
        print("Example: python3 ballSortSolver.py puzzle.json")
        exit()
    else:
        jsonFile = open(sys.argv[1],)

    ballDataJson = json.load(jsonFile)

    ballData = []
    #convert json to list of lists (which will be treated as stacks)
    for row in ballDataJson["puzzle"]:
        ballData.append(row)

    #start from scratch
    solved = solve(ballData, 0)

    if(solved):
        print("Solved!")
    else:
        print("Unsolvable!")