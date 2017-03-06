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

    def __init__(self, piece, file, rank):
        self._piece = piece
        self._rank = rank
        self._file = file
        self._moveCoords.clear()
        self._moveCoords.append(rank)
        self._moveCoords.append(file)

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
            if(state.board.get(keyCheck) == None):
                if(newRank >= 1 and newRank <= 8 ):
                    newMove = move(x, x.file, newRank)
                    possibleMoves.append(newMove)
            #pawn capturing, file +/- 1
            print("checking pawn cap")
            for off in range (-1,2,2):
                newRank = x.rank + state.player.dir
                newFile = chr(ord(x.file) + off)
                keyCheck = coord_to_key(newFile, newRank)
                print("capture check at ",keyCheck)
                capPiece = state.board.get(keyCheck)
                if capPiece != None:
                    print("something is there")
                if(capPiece != None and capPiece.owner.id != state.player.id):
                    print("pawn can capture")
                    newMove = move(x, newFile, newRank)
                    possibleMoves.append(newMove)


    return possibleMoves
            #x.move(chr(ord(x.file) + 1), x.rank + self.player._rank_direction * 2)
            #break


def coord_to_key(file, rank):
    return (str(file) + str(rank))

