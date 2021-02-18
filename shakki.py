import copy
from operator import itemgetter
from os import path
from os import listdir
import random
import sys


class Board:
    def __init__(self, boardstate, history, points):
        self.boardstate = boardstate
        self.height = len(boardstate)
        self.width = len(boardstate[0])
        self.history = history
        self.points = points
    
    def __str__(self):
        st = ""
        for row in range(self.height):
            st = st + "".join(self.boardstate[row]) + "\n"
        st = st + "Moves: " + str(len(self.history)) + "\n"
        st = st + "Points: " + str(self.points) + "\n"
        return st
    
    def win(self):
        king = False
        for row in range(self.height):
            king = king or 'K' in self.boardstate[row]
        if not king:
            finalScore = 0
            pointsmap = dict(zip(('p', 'h', 'b', 'r', 'q', 'k', '-'), (1, 3, 4, 5, 9, 100000, 0)))
            for row in self.boardstate:
                for elem in row:
                    finalScore = finalScore + pointsmap.get(elem, 0)
            self.points = finalScore
        return not king
    
    def print_to_file(self, pos, filename):
        with open(filename, 'a+') as text_file:
            print(f"-----------------------------------\nSolution #{pos}", file=text_file)
            for hist in self.history:
                st = ""
                for row in range(self.height):
                    st = st + "".join(hist[row]) + "\n"
                print(st, file=text_file)
            print(self, file=text_file)
        return

def print_level(maptext, filename, points, moves):
    with open(filename, "w") as text_file:
        last_char = ""
        for char in maptext:
            if(last_char != ""):
                print(last_char, file=text_file, end="")
                if(char != "\n" and last_char != "\n"):
                    print(" ", file=text_file, end="")
            last_char = char
        print("", file=text_file)
        print("#", file=text_file)
        print(points, file=text_file, end=" ")
        print(moves, file=text_file, end="")
    return
                

def makeAImove(boardstate, height, width):
    #Find all moves for AI and select the best one. If no moves, return the original.
    possibleMoves = list()
    for x in range(width):
        for y in range(height):

            #Check pawn
            if(boardstate[y][x]=='P'):
                #One left-Down
                newX = x-1
                newY = y+1
                #Can the piece move?
                if(newX>=0 and newY<height):
                    target = boardstate[newY][newX]
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('p'), y, x, newY, newX))

                #One right-Down
                newX = x+1
                newY = y+1
                #Can the piece move?
                if(newX<width and newY<height):
                    target = boardstate[newY][newX]
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('p'), y, x, newY, newX))
  
            #Check knight
            if(boardstate[y][x]=='H'):
                changes = ((-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (2, -1), (-2, 1), (2, 1))
                for change in changes:
                    newX = x + change[0]
                    newY = y + change[1]
                    #Can the piece move?
                    if(newX>=0 and newY>=0 and newX<width and newY<height):

                        target = boardstate[newY][newX]
                        #Is there something to eat?
                        if(target.islower()):
                            possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('h'), y, x, newY, newX))

            #Check king
            if(boardstate[y][x]=='K'):
                changes = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
                for change in changes:
                    newX = x + change[0]
                    newY = y + change[1]
                    #Can the piece move?
                    if(newX>=0 and newY>=0 and newX<width and newY<height):

                        target = boardstate[newY][newX]
                        #Is there something to eat?
                        if(target.islower()):
                            possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('k'), y, x, newY, newX))

            #Check rook
            if(boardstate[y][x]=="R"):
                #Up
                free = True
                newY = y-1
                newX = x
                while newY>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('r'), y, x, newY, newX))
                    newY -= 1

                #Down
                free = True
                newY = y+1
                newX = x
                while newY<height and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('r'), y, x, newY, newX))
                    newY +=1

                #Left
                free = True
                newY = y
                newX = x-1
                while newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('r'), y, x, newY, newX))
                    newX -= 1
                
                #Right
                newY = y
                newX = x+1
                free = True
                while newX<width and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('r'), y, x, newY, newX))
                    newX += 1
            
            #Check bishop
            if(boardstate[y][x]=="B"):
                #Up-left
                free = True
                newY = y-1
                newX = x-1
                while newY>=0 and newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('b'), y, x, newY, newX))
                    newY -= 1
                    newX -= 1

                #Down-left
                free = True
                newY = y+1
                newX = x-1
                while newY<height and newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('b'), y, x, newY, newX))
                    newY +=1
                    newX -=1

                #Up-right
                free = True
                newY = y-1
                newX = x+1
                while newY>=0 and newX<width and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('b'), y, x, newY, newX))
                    newY -= 1
                    newX += 1
                
                #Down-right
                newY = y+1
                newX = x+1
                free = True
                while newX<width and newY<height and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('b'), y, x, newY, newX))
                    newY += 1
                    newX += 1
                        #Check bishop
            
            #Check queen
            if(boardstate[y][x]=="Q"):
                #Up
                free = True
                newY = y-1
                newX = x
                while newY>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY -= 1

                #Down
                free = True
                newY = y+1
                newX = x
                while newY<height and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY +=1

                #Left
                free = True
                newY = y
                newX = x-1
                while newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newX -= 1
                
                #Right
                newY = y
                newX = x+1
                free = True
                while newX<width and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newX += 1
                
                #Up-left
                free = True
                newY = y-1
                newX = x-1
                while newY>=0 and newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY -= 1
                    newX -= 1

                #Down-left
                free = True
                newY = y+1
                newX = x-1
                while newY<height and newX>=0 and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY +=1
                    newX -=1

                #Up-right
                free = True
                newY = y-1
                newX = x+1
                while newY>=0 and newX<width and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY -= 1
                    newX += 1
                
                #Down-right
                newY = y+1
                newX = x+1
                free = True
                while newX<width and newY<height and free:
                    target = boardstate[newY][newX]
                    #Is it a free tile?
                    free = target=='-'
                    #Is there something to eat?
                    if(target.islower()):
                        possibleMoves.append((-1*pointsmap.get(target), pointsmap.get('q'), y, x, newY, newX))
                    newY += 1
                    newX += 1
    #If no moves or player, return original
    def checkWin(bs):
        for row in bs:
            for elem in row:
                if (elem == 'K'):
                    return False         
        return True

    if(len(possibleMoves)==0 or checkWin(boardstate)):
        return boardstate
    else:
        #Sort by target value, then eating piece value, then by x-coordinate, first target and then eating piece (pick leftmost) 
        possibleMoves.sort(key=itemgetter(0, 1, 5, 3))
        move = possibleMoves[0]
        newBoardstate = copy.deepcopy(boardstate)

        newBoardstate[move[4]][move[5]] = boardstate[move[2]][move[3]]
        newBoardstate[move[2]][move[3]] = '-'
        return newBoardstate

def checkMoves(board):
    possibleBoardstates = list()
    #Create every possible boardstate after a player move
    for x in range(board.width):
        for y in range(board.height):
            #Gather every move
            possibleMoves = list()

            if(board.boardstate[y][x] == '-'): pass

            #Check queen
            if(board.boardstate[y][x]=='q'):
                #Left
                newX = x-1
                newY = y
                while(newX>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX -= 1

                #Right
                newX = x+1
                newY = y
                while(newX<board.width and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX += 1

                #Up
                newX = x
                newY = y+1
                while(newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY += 1

                #Down
                newX = x
                newY = y-1
                while(newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1

                #Left-Up
                newX = x-1
                newY = y+1
                while(newX>=0 and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX -= 1
                    newY += 1

                #Right-Up
                newX = x+1
                newY = y+1
                while(newX<board.width and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX += 1
                    newY += 1

                #Left-Down
                newX = x-1
                newY = y-1
                while(newX>=0 and newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1
                    newX -= 1

                #Right-Down
                newX = x+1
                newY = y-1
                while(newX<board.width and newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1
                    newX += 1
                
            #Check rook
            if(board.boardstate[y][x]=='r'):
                #Left
                newX = x-1
                newY = y
                while(newX>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX -= 1

                #Right
                newX = x+1
                newY = y
                while(newX<board.width and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX += 1

                #Up
                newX = x
                newY = y+1
                while(newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY += 1

                #Down
                newX = x
                newY = y-1
                while(newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1

            #Check bishop
            if(board.boardstate[y][x]=='b'):
                #Left-Up
                newX = x-1
                newY = y+1
                while(newX>=0 and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX -= 1
                    newY += 1

                #Right-Up
                newX = x+1
                newY = y+1
                while(newX<board.width and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newX += 1
                    newY += 1

                #Left-Down
                newX = x-1
                newY = y-1
                while(newX>=0 and newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1
                    newX -= 1

                #Right-Down
                newX = x+1
                newY = y-1
                while(newX<board.width and newY>=0 and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                    possibleMoves.append((newY, newX))
                    if(board.boardstate[newY][newX].isupper()): break
                    newY -= 1
                    newX += 1

            #Check knight
            if(board.boardstate[y][x]=='h'):
                changes = ((-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (2, -1), (-2, 1), (2, 1))
                for change in changes:
                    newX = x + change[0]
                    newY = y + change[1]
                    if(newX>=0 and newY>=0 and newX<board.width and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                        possibleMoves.append((newY, newX))
            
            #Check king
            if(board.boardstate[y][x]=='k'):
                changes = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
                for change in changes:
                    newX = x + change[0]
                    newY = y + change[1]
                    if(newX>=0 and newY>=0 and newX<board.width and newY<board.height and (board.boardstate[newY][newX]=='-'or board.boardstate[newY][newX].isupper())):
                        possibleMoves.append((newY, newX))
            
            #Check pawn
            if(board.boardstate[y][x]=='p'):
                #Up
                newX = x
                newY = y-1
                if newY>=0 and board.boardstate[newY][newX]=='-':
                    possibleMoves.append((newY, newX))
                
                #Left-up
                newX = x-1
                newY = y-1
                if newY>=0 and newX>=0 and board.boardstate[newY][newX].isupper():
                    possibleMoves.append((newY, newX))

                #Right-up
                newX = x+1
                newY = y-1
                if newY>=0 and newX<board.width and board.boardstate[newY][newX].isupper():
                    possibleMoves.append((newY, newX))

            for move in possibleMoves:
                newY, newX = move
                #Add points player eats something else than king
                if(board.boardstate[newY][newX]!='K'):
                    newPoints = board.points + pointsmap.get(board.boardstate[newY][newX].lower())
                newPoints = 0 #Fix later
                newState = copy.deepcopy(board.boardstate)
                newState[y][x] = '-'
                newState[newY][newX] = board.boardstate[y][x]
                possibleBoardstates.append((newState, newPoints))

    #Check AI for each boardstate
    finalBoardstates = [(makeAImove(state, board.height, board.width), newPoints) for (state, newPoints) in possibleBoardstates]

    #Transform possibleBoardstates into a list of boards and remove any with repeated moves
    history = copy.deepcopy(board.history)

    history.append(board.boardstate)
    finalBoardstates = filter(lambda state: not state[0] in history, finalBoardstates)

    return list(Board(state, history, newPoints) for (state, newPoints) in finalBoardstates)

#Maptext should be something like:
maptext_example = """RHBQKBHR
PPPPPPPP
--p-----
--------
--------
PP--P---
p-------
rhbqkbhr
"""

pointsmap = dict(zip(('p', 'h', 'b', 'r', 'q', 'k', '-'), (1, 3, 4, 5, 9, 100000, 0)))
#Filename is name for output file

def calculate_solutions(maptext, filename, target = False, verbose = True):
    #Initialize variables

    best_moves = -1
    best_points = 0
    maplist = maptext.split("\n")
    width = len(maplist[0])
    height = len(maplist) - 1

    board = [[maplist[y][x] for x in range(width)] for y in range(height)]
    history = list()

    start = Board(board, history, 0)

    queue = list()
    visited = set()
    wins = list()
    winset = set()

    queue.append(start)
    visited.add(str(start.boardstate))
    turns = 0


    #Print to console and file
    print("Calculating possible solutions to ChessPuzzle task",
        "--------------------------------------------------",
        "Starting position ",
        start, sep="\n")
    
    with open(filename, 'w') as text_file:
        print("Calculating possible solutions to ChessPuzzle task",
        "--------------------------------------------------",
        "Starting position ",
        start, sep="\n", file=text_file)


    #Run exhaustive breadth-first and print any solutions found to file
    while len(queue)>0:
        board = queue.pop(0)
        li = checkMoves(board)
        if len(board.history)>=turns:
            print("Turn calculated:", turns)
            print("Queue length:", len(queue))
            turns += 1

        for b in li:
            if b.win() and not str(b.boardstate) in winset:
                if(best_moves == -1 or best_moves >= len(b.history)):
                    best_moves = len(b.history)
                    if(best_points < b.points):
                        best_points = b.points
                wins.append(b)
                visited.add(str(b.boardstate))
                winset.add(str(b.boardstate))
                print("Wins found:", len(wins))
                print("Best moves: ", best_moves)
                print("Best points: ", best_points)
                if(target and best_moves < target):
                    return -1, -1
                b.print_to_file(len(wins), filename)
                continue

            if not str(b.boardstate) in visited:
                queue.append(b)
                visited.add(str(b.boardstate))

    return best_moves, best_points

#Calling for .map files from console
if __name__ == "__main__":
    
    if len(sys.argv)<3:
        print("Not enough given parameters! (Needs mode, input_filename, output_filename)")
        sys.exit()
    mode = sys.argv[1]
    if(mode == "solve"):
        file_in = sys.argv[2]
        
        if not path.exists(file_in):
            print("No input file found with given path:", file_in)
            sys.exit()

        file_out = sys.argv[3]
        
        maptext = ""
        with open(file_in, "r") as f:
            for line in f:
                if line[0]=='#':
                    break
                maptext += line.replace(" ", "")
        calculate_solutions(maptext, file_out)

    elif(mode == "create"):
        print("LOL")
        if len(sys.argv)<5:
            print("Not enough given parameters! (Needs mode, size, pieces_amount, moves, output_filename)")
            sys.exit()
        size = int(sys.argv[2])
        pieces_amount = int(sys.argv[3])
        moves = int(sys.argv[4])
        file_out = (sys.argv[5])

        if(pieces_amount > size * size):
            pieces_amount = size * size
        
        successful = False

        while not successful:
            pieces = pieces_amount - 1
            possible_pieces = ['P', 'H', 'B', 'R', 'Q', 'p', 'h', 'b', 'r', 'q']
            chosen_pieces = ["K"]
            for i in range(size*size - 1):
                if(pieces > 0):
                    chosen_pieces.append(possible_pieces[random.randint(0, len(possible_pieces)-1)])
                    pieces = pieces - 1
                else:
                    chosen_pieces.append("-")
            random.shuffle(chosen_pieces)

            maptext = ""
            for x in range(size):   
                for y in range(size):
                    maptext += chosen_pieces.pop()
                maptext += "\n"
            bm, bp = calculate_solutions(maptext, "./solutions/test_random.map", moves)
            if(bm == moves):
                print_level(maptext, "./solutions/solution_random.map", bp, bm)
                successful = True
        
    else:
            sys.exit()