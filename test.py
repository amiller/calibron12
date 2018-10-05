pieces = [(32,11,'x'),
          (32,10,'*'),
          (28,14,'x'),
          (28,7,'-'),
          (28,6,'*'),
          (21,18,'x'),
          (21,18,'+'),
          (21,14,'-'),
          (21,14,'*'),
          (17,14,'-'),
          (14,4,'-'),
          (10,7,'-'),
]



# Python3 program to print sums of 
# all possible subsets. 
  
# Prints sums of all subsets of arr[l..r] 
def subsetSums(arr, l, r, sum = 0): 
      
    # Print current subset 
    if l > r: 
        print (sum, end = " ") 
        return
  
    # Subset including arr[l] 
    subsetSums(arr, l + 1, r, sum + arr[l]) 
  
    # Subset excluding arr[l] 
    subsetSums(arr, l + 1, r, sum) 
  
# Driver code 
arr = [5, 4, 3] 
n = len(arr) 
subsetSums(arr, 0, n - 1) 
  
# This code is contributed by Shreyanshi Arun. 

height = width = 56
assert sum(x*y for x,y,_ in pieces) == height * width

def count_all_holes(board):
    # Returns a set of all integers for which there is an x or y hole
    def count_all_holes(arr):
        i = 0
        holes = []
        while i < len(arr):
            # Find the start of a hole
            while i < len(arr) and arr[i] != ' ':
                i += 1
            start = i
            i += 1
            # Find the end of a hole
            while i < len(arr) and arr[i] == '  ':
                i += 1
            stop = i
            hole = stop  start
            holes.add(hole)

def print_board(board):
    for row in board:
        print(''.join(row))

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
    print_board(board)

draw_board([[10,20,0],
            [10,11,0]])

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

def unapply_piece(piece, conf, board):
    w,h,c = piece
    x,y,o = conf
    if o: (h,w) = (w,h)
    if x < 0 or x+w > width: raise Exception
    if y < 0 or y+h > height: raise Exception
    for i in range(y,y+h):
        for j in range(x,x+w):
            assert board[i][j] != ' '
            board[i][j] = ' '
    return board


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

def _backtrack2(confs, pieces):
    # Try all combinations of next piece
    p,rest = pieces[0],pieces[1:]
    w,h,c = p

    for o in range(2):
        if o: (h,w) = (w,h)
        for x in range(width-w):
            for y in range(height-h):
                # Check if adding this piece is OK
                if not test_conf(confs, p, (x,y,o)): continue
                newconf = confs + ((x,y,o),)
                if rest == []:
                    print('Done!')
                    return newconf
                if len(confs) == 6:
                    draw_board(newconf)
                solved = _backtrack2(newconf,rest)
                if solved: return solved
    return None

#draw_board([[10,20,0],
#            [10,11,0]])

#_backtrack2((), pieces)


            

