class piece:
    _type = None
    _rank = 0
    _file = ""
    _key = ""
    _owner = ""
    _id = ""
    _has_moved = False
    _allow_enPass = False

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

    def set_key(self):
        self._key = str(self._file) + str(self._rank)

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

    def toString(self):
        pieceString = self._owner.color + self._type + "@" + self._file + str(self._rank)
        return pieceString

    @property
    def enPass(self):
        return self._allow_enPass

    def set_enPass(self, bool):
        self._allow_enPass = bool

class player:
    _in_check = False
    _rank_direction = 0
    _name = ""
    _id = ""
    _color = None

    def __init__(self, check, dir, name, id, color):
        self._rank_direction = dir
        self._in_check = check
        self._name = name
        self._id = id
        self._color = color

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

    @property
    def color(self):
        return self._color

    def toString(self):
        string = "Player " + str(self._id) + " is " + self._color
        string += " rank_dir = " + str(self._rank_direction) + " check = " + str(self._in_check)
        return string

class state:

    _board = {}
    _myPieces = []
    _oppPieces = []
    _player = None
    _opponent = None
    _my_id = None
    _fen = ""
    _fen_cast = None
    _fen_enPass = None
    _last_move = None
    _player_in_check = False
    _state_eval = 0


    def __init__(self, player, opp, my_id):
        self._board = {}
        self._myPieces = []
        self._oppPieces = []
        self._player = player
        self._opponent = opp
        self._my_id = my_id

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

    def addOppPiece(self,piece):
        self._oppPieces.append(piece)

    @property
    def oppPieces(self):
        return self._oppPieces

    def resetState(self):
        self._board.clear()
        self._myPieces.clear()
        self._oppPieces.clear()
        self._fen = None

    @property
    def player(self):
        return self._player

    @property
    def opponent(self):
        return self._opponent

    def set_player(self, player):
        self._player = player

    def set_opponent(self, player):
        self._opponent = player

    @property
    def my_id(self):
        return self._my_id

    def add_init_fen(self, fen):
        self._fen = fen
        splitFen = fen.split(" ")
        self._fen_cast = splitFen[2]
        self._fen_enPass = splitFen[3]

    @property
    def fen_cast(self):
        return self._fen_cast

    @property
    def fen_enPass(self):
        return self._fen_enPass

    def set_last_move(self,last_move):
        self._last_move = last_move

    @property
    def last_move(self):
        return self._last_move

    def set_player_check(self,check):
        self._player_in_check = check

    @property
    def player_in_check(self):
        return self._player_in_check

    @property
    def state_eval(self):
        return self._state_eval

    def set_state_eval(self, val):
        self._state_eval = val

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

    def toString(self):
        moveString = self.piece.type + " to " + str(self.file) + str(self.rank)
        return moveString
