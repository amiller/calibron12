# Definition of Calibron12 problem
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

# Diagnostics
def print_board(board):
    for row in board[::2]:
        print(''.join(row))

# Draw from a (partial) conf, printing all Errors 'E'
def draw_board(conf):
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

#### Good version
### Backtracking keeping board as state

# Draw a piece onto a board (modifies board in place)
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

# Draw a piece onto a board (modifies board in place)
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

# good bactracking
_iters = 0
def _backtrack3(board,pieces):

    # Find the next corner to place
    def findNext(board):
        for x in range(width):
            for y in range(height):
                if board[y][x] == ' ': return (x,y)
    x,y = findNext(board)
    
    # Try all choices of next piece
    for pi in range(len(pieces)):
        rest = pieces[:pi] + pieces[pi+1:]
        p = pieces[pi]

        w,h,c = p
        for o in range(2):
            if o: (h,w) = (w,h)
            if not apply_piece(p, (x,y,o), board):
                continue # Couldn't fit
            if rest == []:
                print("\x1b[2J\x1b[H")
                print_board(board)
                print('Done!')
                #return board
            #if len(rest) == 8:
            global _iters
            #if _iters % 10000 == 0:
            #    print("\x1b[2J\x1b[H")
            #    print_board(board)
            _iters += 1
            solved = _backtrack3(board,rest)
            if solved: return solved
            unapply_piece(p, (x,y,o), board)
    return None


############ Version 1
# naive bactracking
def _backtrack(board,pieces):
    from copy import deepcopy
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
                if rest == []:
                    print('Done!')
                    return newboard
                if len(rest) < 5:
                    print_board(newboard)
                solved = _backtrack(newboard,rest)
                if solved: return solved
                unapply_piece(p, (x,y,o), board)
    return None

#### Version 3

#draw_board([[10,20,0],
#            [10,11,0]])

# Achievable dimensions
_dim_cache = {}
def all_dimensions(pieces):
    pieces = tuple(pieces)
    if pieces not in _dim_cache:
        _dim_cache[pieces] = sorted([w for w,h,_ in pieces] + [h for w,h,_ in pieces])[::-1]
    return _dim_cache[pieces]


# Find the sizes of any hole in row or column
def find_all_holes(board):
    def find_holes_in_row(row):
        holes = set()
        i = 0
        while i < len(row):
            # Move i to the start of a hole
            while i < len(row) and row[i] != ' ':
                i += 1
            start = i
            # Find the end of the row
            while i < len(row) and row[i] == ' ':
                i += 1
            stop = i
            if stop - start > 0:
                holes.add(stop - start)
        return holes
    holes = set.union(*map(find_holes_in_row, board))
    #print('holes1:', holes)
    bt = [[board[i][j] for i in range(width)] for j in range(height)]
    holes = holes.union(*map(find_holes_in_row, bt))
    #print('holes:',holes)
    return holes

#board = [[' '] * height for _ in range(width)]
#_backtrack(board, pieces)

def rect_intersect(x,y,w,h, _x,_y,_w,_h):
    if _x >= x+w or x >= _x + _w: return False
    if _y >= y+h or y >= _y + _h: return False
    return True

def test_conf(confs, p, conf):
    # Test if piece p at conf collides with confs
    w,h,c = p
    x,y,o = conf
    if o: (h,w) = (w,h) # flip
    for (_p,_conf) in zip(pieces, confs):
        _w,_h,_ = _p
        _x,_y,_o = _conf
        if _o: (_h,_w) = (_w,_h)
        if rect_intersect(x,y,w,h, _x,_y,_w,_h):
            return False
    return True


###############
# Prints all possible sums of a subset
_sum_cache = {}
def possibleSums(coins):
    if tuple(coins) in _sum_cache:
        return _sum_cache[tuple(coins)]
    total = min(width,sum(coins)) # Total size
    possible = [[] for _ in range(total+1)]
    possible[0] = []
    for coin in coins:
        for i in range(total-coin,-1,-1):
            if possible[i] is not []:
                possible[i+coin] = possible[i]+[coin]
    rs = set([i for i in range(total+1) if possible[i]])
    _sum_cache[tuple(coins)] = rs
    return rs

# Driver code 
#arr = [5, 5, 4, 3]
#print(possibleSums(arr))


###########


print('all dimensions:', all_dimensions(pieces))
print('all achievable dimensions:', possibleSums(all_dimensions(pieces)))


# Backtracking just by comparing figures
def _backtrack2(board, confs, pieces):
    # Try all combinations of next piece
    p,rest = pieces[0],pieces[1:]
    w,h,c = p

    #board = draw_board(confs)

    # Find all of the holes (rows or columns)
    holes = sorted(find_all_holes(board))

    # Find the possible dimensions of the rest
    dims = all_dimensions(pieces=[p]+rest)
    possible = possibleSums(dims)

    # Reject by sums
    if set(holes).difference(possible):
        return None

    # Print the progress so far
    if len(rest) == 5:
        import os
        print("\x1b[2J\x1b[H")
        print_board(board)
        print('all achievable dimensions:', sorted(possibleSums(all_dimensions([p]+rest))))
        print('all holes:', holes)

    firstPiece = len(confs) == 0
        
    # 1. Enumerate the orientation o (0,1)
    for o in range(2):
        if o: (h,w) = (w,h)
        if firstPiece and o == 1: continue
        # 2. Enumerate the x,y positions
        for x in range(width-w):
            # First piece is fixed orientation
            if firstPiece and x > (56 - w+1)//2: continue

            for y in range(height-h):
                # First piece is fixed orientation
                if firstPiece and y > (56 - h+1)//2: continue

                #if board[x][y] != ' ': continue

                # Check if adding the piece p at x,y,o is feasible
                #if not test_conf(confs, p, (x,y,o)): continue
                if not apply_piece(p, (x,y,o), board): continue
                newconf = confs + ((x,y,o),)

                # Check if done
                if rest == []:
                    print('Done!')
                    return newconf

                # Recurse
                solved = _backtrack2(board, newconf,rest)
                if solved: return solved
                else: unapply_piece(p, (x,y,o), board)
    return None

#draw_board([[10,20,0],
#            [10,11,0]])

#_backtrack2(draw_board(()), (), pieces)
_backtrack3(draw_board(()), pieces)


            

