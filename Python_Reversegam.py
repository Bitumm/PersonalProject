import random
import sys
WIDTH = 8
HEIGHT = 8

def drawBoard(board):
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' %(y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')


def getNewBoard():
    # Create a brand-new, blank board data structure
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, mark, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if mark == 'X':
        otherMark = 'O'
    else:
        otherMark = 'X'
    marksToFlip = []
    for xdirection, ydirection in [[0, 1], [1,1], [1,0], [1,-1], [0, -1] , [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        while isOnBoard(x, y) and board[x][y] == otherMark:
            x += xdirection
            y += ydirection
            if isOnBoard(x, y) and board[x][y] == mark:
                # There are pieces to flip over. Go tin the reverse direction until we reach the original space.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    marksToFlip.append([x, y])

    if len(marksToFlip) == 0:
        #there is no mark were flipped, this is a valid move return false.
        return False
    return marksToFlip

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1 
                    
def getBoardWithValidMoves(board, mark):
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(board, mark):
        boardCopy[x][y] = '.'
    return boardCopy

def getValidMoves(board, mark):

    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, mark, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def enterPlayerMark():
    # Let me to enter which mark i want to be.
    # Return a list will the player's mark as the first item and the computer's 
    mark = ''
    while not(mark == 'X' or mark == 'O'):
        print('do you want to be X or O')
        mark = input().upper()

    if mark == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
    

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, mark, xstart, ystart):
    # Place the mark on the board at xstart, ystart and flip any of the opponent's pieces.
    # Return False if this is an invalid else true
    
    marksToFlip = isValidMove(board, mark, xstart, ystart)

    if marksToFlip == False:
        return False
    board[xstart][ystart] = mark
    for x, y in marksToFlip:
        board[x][y] = mark
    return True 

def getBoardCopy(board):
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def getPlayerMove(board, playerMark):
    # Let the player enter their move.
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()

    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerMark, x, y) == False:
                continue
            else:
                break 
        else:
            print('That is not a valid move. Enter the column(1-8) and then row (1-8).')
            print('For example, 81 will be on the top-right corner.')
            
    return [x, y]
    
def getComputerMove(board, computerMark):
    possibleMoves = getValidMoves(board, computerMark)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerMark, x, y)
        score = getScoreOfBoard(boardCopy)[computerMark]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def printScore(board, playerMark, computerMark):
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s point.' %(scores[playerMark], scores[playerMark]))
    
def playGame(playerMark, computerMark):
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first')

    #clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3]='X'
    board[3][4]='O'
    board[4][3]='O'
    board[4][4]='X'
    while True:
        playerValidMoves = getValidMoves(board, playerMark)
        computerValidMoves = getValidMoves(board, computerMark)


        if playerValidMoves == [] and computerValidMoves == []:
            return board
            
        elif turn == 'player':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerMark)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerMark, computerMark)
                
                move = getPlayerMove(board, playerMark)
                
                if move == 'quit':
                    print('Thanks for playing')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerMark, move[0], move[1])
            turn = 'computer'
            
        elif turn == 'computer':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerMark, computerMark)

                input('Press enter to see the computer \'s move.')
                move = getComputerMove(board, computerMark)
                makeMove(board, computerMark, move[0], move[1])
                
            turn = 'player'
print('Welcome to Reversegam!')

playerMark, computerMark = enterPlayerMark()
while True:
    finalBoard = playGame(playerMark, computerMark)

    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored %s points, O scored %s points ! Congrat !' % (scores['X'],scores['O']))

    if scores[playerMark] > scores[computerMark]:
        print('You won')
    elif scores[playerMark] < scores[computerMark]:
        print('You lost')
    else:
        print('The game was a tie!')
        
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break

    

            
            

























        



                

            
            
            
        
        
        
    
    
    
