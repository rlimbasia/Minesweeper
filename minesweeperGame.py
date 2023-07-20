import numpy
from queue import Queue
#from minesweeperAgents import randomAgent



def neighborIndex(pos, boardSize):
    """For a given position, returns the indices of all the neighbors

    Parameters
    -----------
    pos: 2-tuple
        valid coordinates of any tile on the board
    
    boardSize: 2-tuple
        dimensions of the board in the form (rows, columns)
    
    Returns
    --------
    neighbors
        array of 2-tuples, each tuple gives the coordinates of a tile adjacent to pos
    """
    row, col = pos

    neighbors = numpy.empty(9, dtype=object)
    for i in range(len(neighbors)):
        if (i<3):
            neighbors[i] = (row-1,col-1+i)
        elif (i<6):
            neighbors[i] = (row,col-4+i)
        else:
            neighbors[i] = (row+1,col-7+i)

    invalidIndex = numpy.full(9, -1)

    for i in range(len(invalidIndex)):
        if ( neighbors[i][0] < 0 or neighbors[i][1] < 0 or neighbors[i][0] > boardSize[0]-1 or neighbors[i][1] > boardSize[1]-1):
            invalidIndex[i] = i
    

    invalidIndex = invalidIndex[invalidIndex!=-1]
    invalidIndex = numpy.append(invalidIndex, 4)

    neighbors = numpy.delete(neighbors, invalidIndex)

    return neighbors





def createBoard(rows,cols,mineCount,firstMove):
    """Creates a consistent minesweeper board

    Parameters
    -----------
    rows: int
        number of rows in the board
    
    cols: int
        number of columns in the board

    mineCount: int
        number of mines in the board, must be less than rows*cols + 1

    Returns
    --------
    board
        2D array with mines randomly placed and all non-mine tiles containing the number of mines adjacent to it
    """

    board = numpy.zeros((rows,cols))

    rng = numpy.random.default_rng()
    minePositions = numpy.arange(rows*cols)
    rng.shuffle(minePositions)
    notMinePositions = numpy.sort(minePositions[mineCount:])
    minePositions = numpy.sort(minePositions[:mineCount])
    

    fmX, fmY = firstMove
    fmPos = 16*fmX + fmY
    

    x = numpy.argwhere(minePositions==fmPos)  # if our first move has a mine, x will give the index of it in minePositions
    

    # if x is nonempty, then we swap out our first move with the next random mine position
    if(len(x) > 0):
        minePositions = numpy.delete(minePositions, x[0])
        minePositions = numpy.insert(minePositions, 0, notMinePositions[0])


    for i in range(len(minePositions)):
        m = minePositions[i]
        board[ int((m - m%cols)/cols) ][ m%cols ] = -1

    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] == -1):
                neighbors = neighborIndex((i,j),(rows,cols))
                for k in range(len(neighbors)):
                    if (board[ neighbors[k][0] ][ neighbors[k][1] ] != -1):
                        board[ neighbors[k][0] ][ neighbors[k][1] ] += 1
                    

    return board




# seed: initial 0 tile 

#returns a list of the positions of all zeros in a connected component
def floodFill(seed, board, view):

    q = Queue(maxsize = 0)
    q.put(seed)
    boardSize = (len(board),len(board[0]))

    while(q.empty() == False):
        n = q.get()
        nX, nY = n

        if (board[nX][nY] == 0 and view[nX][nY] == -2):
            nodeNeighbors = neighborIndex((nX,nY), boardSize)
            for i in range(len(nodeNeighbors)):
                q.put(nodeNeighbors[i])

        view[nX][nY] = board[nX][nY]


    return board, view




def play(board, playerView, move):
    """Updates the players view based on the players move
    
    Parameters
    -----------
    board: 2D array
        board with all mine information uncovered
    
    playerView: 2D array
        board with (partially) covered tiles
    
    move: 2-tuple
        coordinates of tile that player wishes to uncover

    Returns
    --------
    playerView
        updated view with the move-tile uncovered
    
    "GAME OVER" 
        indicates the move-tile was covering a mine

    "CONT"
        indicates that the game continues
    """

    moveRow, moveCol = move
    moveTile = board[moveRow][moveCol]

    if (moveTile == -1):
        playerView[moveRow][moveCol] = moveTile
        return playerView, "GAME OVER"
    
    elif(moveTile == 0):
        board, playerView = floodFill(move, board, playerView)

        return playerView, "CONT" 
    
    else:
        playerView[moveRow][moveCol] = moveTile

        return playerView, "CONT"





def randomAgent(view):

    rng = numpy.random.default_rng()
    nView = numpy.array(view)
    unclickedTiles = numpy.argwhere(nView==-2)
    tileIndex = rng.integers(0,high=len(unclickedTiles)+1)
    move = tuple(unclickedTiles[tileIndex])
    return move

def inputAgent(view):
    move = input()
    move = tuple(int(x) for x in move.split(","))
    return move


def deterministicAgent(view):
    return




def  gameRunner(boardSize, mineCount,agent):
    """Runs game process 
    
    Parameters
    -----------
    boardSize: 2-tuple
        The size of the board

    mineCount: int
        number of mines

    agent: function
        the player
    """

    view = numpy.full((30,16), -2, dtype=float)
    move = agent(view)
    print(move)
    board = createBoard(boardSize[0],boardSize[1],mineCount,move)

    view, gameState = play(board,view,move)
    print(view)

    while(True):
        move = agent(view)
        print(move)

        newView, gameState = play(board,view,move)

        view = newView

        print(view)

        if (gameState == "GAME OVER"): 
            print(gameState)
            break
        

    return "SUCCESS"


gameRunner((30,16),99,randomAgent)
