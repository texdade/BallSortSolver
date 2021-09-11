import json, sys, copy

#define pass_by_value decorator
def pass_by_value(f):
    def _f(*args, **kwargs):
        args_copied = copy.deepcopy(args)
        kwargs_copied = copy.deepcopy(kwargs)
        return f(*args_copied, **kwargs_copied)
    return _f

def checkMoves(ballData, blockedMoves, current):
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
            if not (current, i) in blockedMoves:
                #put the empty vial move at the back, so more meaningful moves can be done before
                if(not sameColor(ballData[current])):
                    moves.append((current, i))
        #if there is a ball of the same color and the vial isn't full
        elif color == vial[-1] and len(vial) < 4:
            #check if the move isn't blocked
            if not (current, i) in blockedMoves:
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

@pass_by_value
def solve(ballData, blockedMoves, current, fromVial, toVial):
    print(ballData)

    if(current == len(ballData)):
        current = 0

    if(fromVial != -1 and toVial != -1):
        ball = ballData[fromVial].pop()
        ballData[toVial].append(ball)
        blockedMoves.add((toVial, fromVial))

        #remove blocked moves in that vial
        blockedMoves = list(blockedMoves)
        for blockedMove in blockedMoves:
            if(blockedMove[0] == fromVial):
                blockedMoves.remove((blockedMove[0], blockedMove[1]))
        blockedMoves = set(blockedMoves)
       
    if(checkWinCon(ballData)):
        print(ballData)
        return True

    #check possible moves
    moves = checkMoves(ballData, blockedMoves, current)

    #if we don't have moves, check next vial
    if(moves == []):
        return solve(ballData, blockedMoves, current+1, -1, -1)

    for move in moves:
        return solve(ballData, blockedMoves, current, move[0], move[1])

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
    solved = solve(ballData, set(), 0, -1, -1)

    if(solved):
        print("Solved!")
    else:
        print("Unsolvable!")