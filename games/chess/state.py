class piece:
    _type = None
    _rank = 0
    _file = ""
    _key = ""
    _owner = ""
    _id = ""
    _has_moved = False

    def __init__(self, type, file, rank, owner, id, moved):
        self._type = type
        self._rank = rank    #rank is row, value is a number 1-8
        self._file = file    #file is column, value is letter a-h
        self._key =  str(file) + str(rank)
        self._owner = owner
        self._id = id
        self._has_moved = moved

    @property
    def key(self):
        return self._key

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def rank(self):
        return self._rank

    @property
    def file(self):
        return self._file

    @property
    def moved(self):
        return self._has_moved

    @property
    def owner(self):
        return self._owner


class player:
    _in_check = False
    _rank_direction = 0
    _name = ""
    _id = ""


    def __init__(self, check, dir, name, id):
        self._rank_direction = dir
        self._in_check = check
        self._name = name
        self._id = id

    @property
    def check(self):
        return self._in_check

    @property
    def dir(self):
        return self._rank_direction

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


class state:

    _board = {}
    _myPieces = []
    _player = None

    def __init__(self, player):
        self._board = {}
        self._myPieces = []
        self._player = player

    def addToBoard(self,piece,key):
        self._board[key] = piece

    @property
    def board(self):
        return self._board

    def addPieces(self, piece):
        self._myPieces.append(piece)

    @property
    def pieces(self):
        return self._myPieces

    def resetState(self):
        self._board.clear()
        self._myPieces.clear()

    @property
    def player(self):
        return self._player


class move:
    _piece = None
    _rank = 0
    _file = 0
    _moveCoords = []
    _proType = None


    def __init__(self, piece, file, rank, proType = None):
        self._piece = piece
        self._rank = rank
        self._file = file
        self._moveCoords.clear()
        self._moveCoords.append(rank)
        self._moveCoords.append(file)
        if proType != None:
            self._proType = proType

    @property
    def coords(self):
        return self._moveCoords

    @property
    def piece(self):
        return self._piece

    @property
    def file(self):
        return self._file

    @property
    def rank(self):
        return self._rank

    @property
    def proType(self):
        return self._proType


def find_actions(state):
    print("finding actions")
    possibleMoves = []
    for x in (state.pieces):
        if x.type == "Pawn":
            #2 square opening move
            if(x.moved == False):
                newRank = x.rank + 2 * state.player.dir
                keyCheck = coord_to_key(x.file, newRank)
                key2 = coord_to_key(x.file, x.rank + state.player.dir)
                if(state.board.get(keyCheck) == None and state.board.get(key2) == None):
                    newMove = move(x, x.file, newRank)
                    possibleMoves.append(newMove)
            #typical one square move
            newRank = x.rank + state.player.dir
            keyCheck = coord_to_key(x.file, newRank)
            #move forward
            if(state.board.get(keyCheck) == None):
                if(newRank > 1 and newRank < 8 ):
                    newMove = move(x, x.file, newRank)
                    possibleMoves.append(newMove)
                #promote pawn if at edge
                elif(newRank == 1 or newRank == 8):
                    for proT in promoteTypes():
                        newMove = move(x, x.file, newRank, proT)
                        possibleMoves.append(newMove)
            #pawn capturing, file +/- 1
            for off in range (-1,2,2):
                newRank = x.rank + state.player.dir
                newFile = chr(ord(x.file) + off)
                keyCheck = coord_to_key(newFile, newRank)
                capPiece = state.board.get(keyCheck)
                #capture the piece if it's there
                if(capPiece != None and capPiece.owner.id != state.player.id):
                    if (newRank > 1 and newRank < 8):
                        newMove = move(x, newFile, newRank)
                        possibleMoves.append(newMove)
                    #capture piece and promote pawn if edge board
                    elif (newRank == 1 or newRank == 8):
                        for proT in promoteTypes():
                            newMove = move(x, newFile, newRank, proT)
                            possibleMoves.append(newMove)
        if x.type == "Knight":
            #knight can move manhattan distance of 3, just not in a straight line
            #check all locations in a 5x5 square around knight with man_dist = 3
            #knight can go there as long as my piece isn't already there
            for r in range (x.rank-2, x.rank+3,1):
                for f in range (ord(x.file)-2, ord(x.file)+3, 1):
                    #location must be on the board
                    if(r >= 1 and r <= 8 and f >= ord('a') and f <= ord('h')):
                        #location must be man_dist of 3 away
                        if(man_dist(ord(x.file), x.rank, f, r) == 3):
                            keyCheck = coord_to_key(chr(f),r)
                            #valid move as long as my piece isn't there
                            capPiece = state.board.get(keyCheck)
                            if(capPiece == None or capPiece.owner.id != state.player.id):
                                newMove = move(x,chr(f),r)
                                possibleMoves.append(newMove)

        if x.type == "Rook":
            #rook can move horizontal/vertical until it hits another piece or edge of the board
            #check from the rook in all 4 directions for valid moves
            cross_moves = check_crossway(state, x.file, x.rank)
            if cross_moves != None:
                for cross_move in cross_moves:
                    newMove = move(x, cross_move[0], cross_move[1])
                    possibleMoves.append(newMove)

        if x.type == "Bishop":
            #bishop can move diagonally in any direction
            diagonal_moves = check_diagonal(state, x.file, x.rank)
            if diagonal_moves != None:
                for diag_move in diagonal_moves:
                    newMove = move(x, diag_move[0], diag_move[1])
                    possibleMoves.append(newMove)

        if x.type == "Queen":
            cross_moves = check_crossway(state, x.file, x.rank)
            diag_moves = check_diagonal(state, x.file, x.rank)
            queen_moves = cross_moves + diag_moves

            if queen_moves != None:
                for queen_move in queen_moves:
                    newMove = move(x, queen_move[0], queen_move[1])
                    possibleMoves.append(newMove)

        if x.type == "King":
            for r in range(x.rank - 1, x.rank + 2, 1):
                for f in range(ord(x.file) - 1, ord(x.file) + 2, 1):
                    # location must be on the board
                    if (r >= 1 and r <= 8 and f >= ord('a') and f <= ord('h')):
                        #not counting it's current position
                        if(r != x.rank and chr(r) != x.file):
                            key = coord_to_key(chr(f),r)
                            capPiece = state.board.get(key)
                            #King can go to empty space or capture opponent piece
                            if(capPiece == None or capPiece.owner.id != state.player.id):
                                newMove = move(x,chr(f),r)
                                possibleMoves.append(newMove)

    return possibleMoves



def coord_to_key(file, rank):
    return (str(file) + str(rank))

def promoteTypes():
    return ('Queen', 'Knight', 'Rook', 'Bishop')

def man_dist(file1, rank1, file2, rank2):
    return abs(file1 - file2) + abs(rank1 - rank2)

def check_crossway(state, p_file, p_rank):
    #print("rook at: ", p_file, p_rank)
    f_ranges = []
    r_ranges = []
    #ranges have (start, stop, increment value)
    if (p_file != 'h'):
        f_ranges.append((chr(ord(p_file) + 1), 'i', 1))
    if (p_file != 'a'):
        f_ranges.append((chr(ord(p_file) - 1), chr(ord('a') - 1), -1))
    if (p_rank != 8):
        r_ranges.append((p_rank + 1, 9, 1))
    if (p_rank != 1):
        r_ranges.append((p_rank - 1, 0, -1))

    valid_move_locations = []
    #list of tuples, (file, rank)

    for f_range in f_ranges:
        for f in range (ord(f_range[0]), ord(f_range[1]), f_range[2]):
            key = coord_to_key(chr(f), p_rank)
            #valid move if empty space
            if state.board.get(key) == None:
                valid_move_locations.append((chr(f), p_rank))
            #valid move if opponent piece, break after
            elif state.board.get(key).owner.id != state.player.id:
                valid_move_locations.append((chr(f), p_rank))
                break
            #cannot move into my own piece
            elif state.board.get(key).owner.id == state.player.id:
                break


    for r_range in r_ranges:
        for r in range (r_range[0], r_range[1], r_range[2]):
            key = coord_to_key(p_file, r)
            #empty space
            if state.board.get(key) == None:
                valid_move_locations.append((p_file, r))
            #capture opponent piece
            elif state.board.get(key).owner.id != state.player.id:
                valid_move_locations.append((p_file, r))
                break
            #my own piece
            elif state.board.get(key).owner.id == state.player.id:
                break

    return valid_move_locations

def check_diagonal(state, p_file, p_rank):

    diagonals = []
    #diagnonals stored as tuples, change in: (file, rank)
    #(1,1),(1,-1),(-1,1),(-1,-1)

    if (p_file < 'h' and p_rank < 8):
        diagonals.append((1,1))
    if (p_file < 'h' and p_rank > 1):
        diagonals.append((1,-1))
    if (p_file > 'a' and p_rank > 1):
        diagonals.append((-1,-1))
    if (p_file > 'a' and p_rank < 8):
        diagonals.append((-1,1))

    valid_move_locations = []

    for diag in diagonals:
        #offset file and rank by the diagonal direction
        f = chr(ord(p_file) + diag[0])
        r = p_rank + diag[1]
        #keep the piece in the board
        while(f >= 'a' and f <= 'h' and r >= 1 and r <= 8):
            key = coord_to_key(f,r)
            #empty space is a valid move
            if(state.board.get(key) == None):
                valid_move_locations.append((f,r))
            #opponents piece is valid, but cannot go further
            elif(state.board.get(key).owner.id != state.player.id):
                valid_move_locations.append((f,r))
                break
            #cannot go past my own piece
            else:
                break

            f = chr(ord(f) + diag[0])
            r += diag[1]

    return valid_move_locations