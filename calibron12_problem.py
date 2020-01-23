# Definition of Calibron12 problem
# Each piece is defined by a width, height, and a "texture"
pieces = [
          (14,4,'-'),
          (28,6,'*'),
          (10,7,'-'),
          (28,7,'-'),
          (32,10,'*'),
          (32,11,'x'),
          (17,14,'-'),
          (28,14,'x'),
          (21,18,'x'),
          (21,18,'+'),
          (21,14,'-'),
          (21,14,'*'),
]
pieces = sorted(pieces)[::-1]

height = width = 56
assert sum(x*y for x,y,_ in pieces) == height * width

# A rendered board is an array of 56 strings, each string with 56 characters
def print_board(board):
    for row in board[::2]:
        print(''.join(row))

def empty_board():
    return [[' '] * height for _ in range(width)]
        

# Render a board given a (partial) configuration, printing all Errors 'E'
# A configuration takes the form:
#  [ ...(x,y,o)... ], a list of (up to) 12 tuples,
#    where in each tuple we have x,y as the location of the top corner
#    of the corresponding piece, and o is either {0,1}, corresponding
#    to horizontal or vertical orientation.
def conf_to_board(conf):
    board = [[' '] * height for _ in range(width)]
    for (w,h,c),(x,y,o) in zip(pieces,conf):
        if o: (h,w) = (w,h) # swap
        for i in range(y,y+h):
            for j in range(x,x+w):
                if board[i][j] != ' ':
                    board[i][j] = 'E'
                else:
                    board[i][j] = c
    return board

# Example
#  Only place the biggest two pieces, both in horizontal position.
#  The pieces partially overlap, resulting in 'E' error characters
print_board(conf_to_board([[10,20,0],
                           [12,11,0]]))


##################################
# Inefficient brute force solution
##################################

# Adds one new piece onto a board, **modifying the board in place**.
# Returns "None" if adding the piece here would create an overlap with
# the pieces already on the board, or if it would go out of bounds.
def apply_piece(piece, conf, board):
    w,h,c = piece
    x,y,o = conf
    if o: (h,w) = (w,h)
    if x < 0 or x+w > width: return None
    if y < 0 or y+h > height: return None
    for i in range(y,y+h):
        for j in range(x,x+w):
            if board[i][j] != ' ': return None
    for i in range(y,y+h):
        for j in range(x,x+w):
            board[i][j] = c
    return board

# This "undoes" the in-place modification of apply_piece.
def unapply_piece(piece, conf, board):
    w,h,c = piece
    x,y,o = conf
    if o: (h,w) = (w,h)
    if x < 0 or x+w > width: return None
    if y < 0 or y+h > height: return None
    for i in range(y,y+h):
        for j in range(x,x+w):
            assert board[i][j] != ' '
            board[i][j] = ' '
    return board


############ Version 1
# naive bactracking
_iters = 0
def _backtrack(board,pieces):
    global _iters
    # Try all combinations of next piece
    p,rest = pieces[0],pieces[1:]
    w,h,c = p
    for o in range(2):
        if o: (h,w) = (w,h)
        for x in range(width-w):
            for y in range(height-h):
                newboard = apply_piece(p, (x,y,o), board)
                if newboard is None:
                    continue
                _iters += 1
                if rest == []:
                    print('Done!')
                    return newboard
                if len(rest) < 5:
                    print 'Board at iteration %d' % (_iters,)
                    print_board(newboard)
                solved = _backtrack(newboard,rest)
                if solved: return solved
                unapply_piece(p, (x,y,o), board)
    return None

# Run this algorithm
_backtrack(empty_board(), pieces)

