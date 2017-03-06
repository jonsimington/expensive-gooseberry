class piece:
    _type = None
    _rank = 0
    _file = ""
    _key = ""
    _owner = ""
    _id = ""

    def __init__(self,type,rank,file,owner, id):
        self._type = type
        self._rank = rank    #rank is row, value is a number 1-8
        self._file = file    #file is column, value is letter a-h
        self._key =  str(file) + str(rank)
        self._owner = owner
        self._id = id

    def getKey(self):
        return self._key

    def getType(self):
        return self._type

    @property
    def id(self):
        return self._id



class state:

    _board = {}
    _myPieces = []

    def __init__(self):
        self._board = {}
        self._myPieces = []

    def addToBoard(self,piece,key):
        self._board[key] = piece

    def getBoard(self):
        return self._board

    def addPieces(self, piece):
        self._myPieces.append(piece)

    def getPieces(self):
        return self._myPieces

    def resetState(self):
        self._board.clear()
        self._myPieces.clear()


class move:
    _piece = None
    _rankOffset = 0
    _fileOffset = 0
    _moveCoords = []

    def __init__(self, piece, rank, file):
        self._piece = piece
        self._rankOffset = rank
        self._fileOffset = file
        self._moveCoords.clear()
        self._moveCoords.append(rank)
        self._moveCoords.append(file)

    @property
    def coords(self):
        return self._moveCoords

    @property
    def piece(self):
        return self._piece


def find_actions(state):
    for x in (state.getPieces()):
        if x.getType() == "Knight":
            newMove = move(x,2,1)
            #newMove.saveMove(newMove,x,2,1)
            return newMove
            #x.move(chr(ord(x.file) + 1), x.rank + self.player._rank_direction * 2)
            #break