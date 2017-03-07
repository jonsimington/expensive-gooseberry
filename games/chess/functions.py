from games.chess.classes import state
from games.chess.classes import piece
from games.chess.classes import move
from games.chess.classes import player
from copy import deepcopy

def find_actions(state, pieces):
    if(state.player.id == state.my_id):
        print("finding actions")
    possibleMoves = []
    for x in (pieces):
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
                #add piece to list if looking for opponent's moves
                if((state.player.id != state.my_id) or (capPiece != None and capPiece.owner.id != state.player.id)):
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

            k_moves = ((1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1))

            for k_mov in k_moves:
                r = (k_mov[0])
                f = (k_mov[1])
                newRank = x.rank + r
                newFile = chr(ord(x.file) + f)
                if(newRank >= 1 and newRank <= 8 and newFile >= 'a' and newFile <= 'h'):
                    key = coord_to_key(newFile, newRank)
                    capPiece = state.board.get(key)
                    if(capPiece == None or capPiece.owner.id == state.opponent.id):
                        newMove = move(x,newFile,newRank)
                        possibleMoves.append(newMove)
                        #if state.player.id == state.my_id:
                            #print("King move added:", newMove.toString())

        '''for r in range(x.rank - 1, x.rank + 2, 1):
                for f in range(ord(x.file) - 1, ord(x.file) + 2, 1):
                    # location must be on the board
                    if (r >= 1 and r <= 8 and f >= ord('a') and f <= ord('h')):
                        #not counting it's current position
                        if(r != x.rank and chr(f) != x.file):
                            key = coord_to_key(chr(f),r)
                            capPiece = state.board.get(key)
                            #King can go to empty space or capture opponent piece
                            if(capPiece == None or capPiece.owner.id == state.opponent.id):
                                newMove = move(x,chr(f),r)
                                if state.player.id == state.my_id:
                                    print("King move added:", newMove.toString())
                                possibleMoves.append(newMove)
                                '''
            #if(x.moved == False):
                #print("castle?")


    #remove moves that put me in check by filtering
    #only do this check for me, not opponent
    #print("checking invalid check moves for player = ", state.player.id)
    if(state.player.id == state.my_id):
        nonCheckMoves = []
        for m in possibleMoves:
            #if m.piece.type == "King":
                #print("checking move: ", m.toString())
            check_state = deepcopy(state)
            m_result = result(check_state,m)
            if(in_check(m_result) == False):
                #if(m.piece.type == "King"):
                   # print("king move won't put him in check")
                nonCheckMoves.append(m)
            #else:
                #print("invalid move skipped")
        #nonCheckMoves = [m for m in possibleMoves if in_check(result(state,m)) == False]
        #print("removed invalid actions which would put me in check, this many:", len(possibleMoves) - len(nonCheckMoves))
    else:
        #print("not me, dont care")
        return possibleMoves

    '''for m in possibleMoves:
        resultant = result(state,m)
        if (in_check(resultant)):
            possibleMoves.remove(m)
            print("move that would result in check removed")'''

    all_considered = []
    all_considered.append(nonCheckMoves)
    all_considered.append(possibleMoves)
    #return nonCheckMoves
    return all_considered


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


def result(state, move):
    #print("result of move: ", move.toString())
    resultant_state = deepcopy(state)
    for p in resultant_state.pieces:
        if move.piece.id == p.id:
            del resultant_state.board[p.key]
            p._rank = move.rank
            p._file = move.file
            #update if pawn is promotoed
            if move.proType != None:
                p._type = move.proType

            p.set_key()
            #if opponent piece captured, delete from board
            oppPiece = resultant_state.board.get(p.key)
            if(oppPiece != None):
                del resultant_state.board[p.key]
                for o in resultant_state.oppPieces:
                    if oppPiece.id == o.id:
                        resultant_state.oppPieces.remove(o)
            #add piece back to board in new location
                resultant_state.addPieces(p)
                resultant_state.addToBoard(p,p.key)
            break

    return resultant_state



def in_check(state):
    checked = False

    me = state.player
    myKing = None

    for p in state.pieces:
        if p.type == "King":
            myKing = p
            break

    check_state = deepcopy(state)
    check_state.set_player(state.opponent)
    check_state.set_opponent(me)

    opp_actions = find_actions(check_state,check_state.oppPieces)

    for oppMove in opp_actions:
        if oppMove.file == myKing.file and oppMove.rank == myKing.rank:
            #print("in check!")
            return True

    return False

    #for oppMove in opp_actions:
    #    if oppMove.file ==


    #for playa in

    return checked