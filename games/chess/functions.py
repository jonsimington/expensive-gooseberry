from games.chess.classes import state
from games.chess.classes import piece
from games.chess.classes import move
from games.chess.classes import player
from copy import deepcopy

def find_actions(state, pieces):
   # if(state.player.id == state.my_id):
        #print("finding actions")
    possibleMoves = []
    for x in (pieces):
        if x.type == "Pawn":
            #2 square opening move
            if(x.moved == False):
                if(x.owner.color == "White" and x.rank == 2) or (x.owner.color == "Black" and x.rank == 7):
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
                #en passant from fen
                if(state.fen_enPass != "-"):
                    if(keyCheck == state.fen_enPass):
                        newMove = move(x, newFile, newRank)
                        possibleMoves.append(newMove)
                #en passant otherwise
                if(state.fen_enPass == '-' or state.fen_enPass == None):
                    if x.file > 'a':
                        lkey = coord_to_key(chr(ord(x.file) - 1), x.rank)
                        if state.board.get(lkey) != None and state.board.get(lkey).type == "Pawn":
                            if state.last_move == "P"+ lkey or state.last_move == "p" + lkey:
                                newMove = move(x, newFile, newRank)
                                possibleMoves.append(newMove)
                    if x.file > 'h':
                        rkey = coord_to_key(chr(ord(x.file) - 1), x.rank)
                        if state.board.get(rkey) != None and state.board.get(rkey).type == "Pawn":
                            if state.last_move == "P" + rkey or state.last_move == "p" + rkey:
                                newMove = move(x, newFile, newRank)
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
            if(state.player.id == state.my_id):
               possibleMoves += check_castle(state,x)

    #remove moves that put me in check by filtering
    #only do this check for me, not opponent
    #if(state.player.id == state.my_id):
    nonCheckMoves = []
    for m in possibleMoves:
        #check_state = deepcopy(state)
        m_result = result(state,m)
        if(m_result.player_in_check == False):
            nonCheckMoves.append(m)
    #else:
        #return possibleMoves

    all_considered = []
    all_considered.append(nonCheckMoves)
    all_considered.append(possibleMoves)

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
                #print("empty space:",key)
            #valid move if opponent piece, break after
            elif state.board.get(key).owner.id != state.player.id:
                valid_move_locations.append((chr(f), p_rank))
                #print("capture piece:", key)
                break
            #cannot move into my own piece
            elif state.board.get(key).owner.id == state.player.id:
                #print("same piece owner:", key)
                break


    for r_range in r_ranges:
        for r in range (r_range[0], r_range[1], r_range[2]):
            key = coord_to_key(p_file, r)
            #empty space
            if state.board.get(key) == None:
                valid_move_locations.append((p_file, r))
                #print("empty space:", key)
            #capture opponent piece
            elif state.board.get(key).owner.id != state.player.id:
                valid_move_locations.append((p_file, r))
                #print("capture piece:", key)
                break
            #my own piece
            elif state.board.get(key).owner.id == state.player.id:
                #print("same piece owner:", key)
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
           # print("checking:", key)
            #empty space is a valid move
            if(state.board.get(key) == None):
                valid_move_locations.append((f,r))
               # print(key, "empty space")
            #opponents piece is valid, but cannot go further
            elif(state.board.get(key).owner.id != state.player.id):
                valid_move_locations.append((f,r))
                #print(key, "opp piece here")
                break
            #cannot go past my own piece
            elif(state.board.get(key).owner.id == state.player.id):
               # print(key, "my piece here")
                break

            f = chr(ord(f) + diag[0])
            r += diag[1]

    return valid_move_locations


def result(state, move):
    #print("result of move: ", move.toString())
    resultant_state = deepcopy(state)
    if resultant_state.player.id == resultant_state.my_id:
        mover_pieces = resultant_state.pieces
        waiter_pieces = resultant_state.oppPieces
    else:
        mover_pieces = resultant_state.oppPieces
        waiter_pieces = resultant_state.pieces
    for p in mover_pieces:
        if move.piece.id == p.id:
            #print ("mover piece is ", p.toString())
            #delete piece from old position on board before move
            del resultant_state.board[p.key]
            #print("delete", p.toString(), "from board")
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
                for o in waiter_pieces:
                    if oppPiece.id == o.id:
                        waiter_pieces.remove(o)
            #add moved piece back to board in new location
            resultant_state.addToBoard(p,p.key)
            break

    if in_check(resultant_state) == True:
        resultant_state.set_player_check(True)
    else:
        resultant_state.set_player_check(False)

    resultant_state.set_last_move(move)
    #print("resultant state for move", move.toString(), ":")
    #print_current_board(resultant_state)
    return resultant_state


def in_check(state, myKing = None):
    if state.player.id == state.my_id:
        pieces = state.pieces
    else:
        pieces = state.oppPieces

    if myKing ==  None:
        for p in pieces:
            if p.type == "King":
                myKing = p
                break

    #check for knights
    for r in range(myKing.rank - 2, myKing.rank + 3, 1):
        for f in range(ord(myKing.file) - 2, ord(myKing.file) + 3, 1):
            # location must be on the board
            if (r >= 1 and r <= 8 and f >= ord('a') and f <= ord('h')):
                # location must be man_dist of 3 away
                if (man_dist(ord(myKing.file), myKing.rank, f, r) == 3):
                    keyCheck = coord_to_key(chr(f), r)
                    oppKnight = state.board.get(keyCheck)
                    if (oppKnight != None and oppKnight.owner.id != myKing.owner.id):
                        if oppKnight.type == "Knight":
                            return True

    #radiate out from king and look for attacking piece
    #4 crossway and 4 diagonal directions to check for pieces
    #if i find a piece with same owner as "my king", stop because it's safe
    #if i find an opponent piece, check what it is depending the direction going
    #make sure to multiply all rank values by state.player.rank_direction (state.player.dir)
    #direcitons are stored as (file, rank)
    myR = state.player.dir
    crossways = ((1, 0), (0, myR), (0, -1 * myR), (-1, 0))
    diagonals = ((1, myR), (1, -1 * myR), (-1, myR), (-1, -1 * myR))

    for dir in crossways:
        f_check = chr(ord(myKing.file) + dir[0])
        r_check = myKing.rank + dir[1]
        while(r_check >= 1 and r_check <= 8 and f_check >= 'a' and f_check <= 'h'):
            key = coord_to_key(f_check, r_check)
            p_check = state.board.get(key)
            if p_check != None:
                if p_check.owner.id != myKing.owner.id:
                    #opponent piece!
                    if r_check == myKing.rank + dir[1] and f_check == chr(ord(myKing.file) + dir[0]):
                        if p_check.type == "King":
                            return True
                    if p_check.type == "Rook" or p_check.type == "Queen":
                        return True
                    else:
                        #not a dangerous piece
                        break
                else:
                    #king's piece
                    break

            f_check = chr(ord(f_check) + dir[0])
            r_check = r_check + dir[1]

    for dir in diagonals:
        f_check = chr(ord(myKing.file) + dir[0])
        r_check = myKing.rank + dir[1]
        while (r_check >= 1 and r_check <= 8 and f_check >= 'a' and f_check <= 'h'):
            key = coord_to_key(f_check, r_check)
            p_check = state.board.get(key)
            if p_check != None:
                if p_check.owner.id != myKing.owner.id:
                    # opponent piece!
                    if r_check == myKing.rank + dir[1] and f_check == chr(ord(myKing.file) + dir[0]):
                        if p_check.type == "King":
                            return True
                    if dir[1] == myR and r_check == myKing.rank + dir[1]:
                        #my direction, look for pawns
                        #only if it's one in front though
                        if p_check.type == "Pawn":
                            return True
                    if p_check.type == "Bishop" or p_check.type == "Queen":
                        return True
                    else:
                        # not a dangerous piece
                        break
                else:
                    #king's piece
                    break

            f_check = chr(ord(f_check) + dir[0])
            r_check = r_check + dir[1]

    return False

def check_mate(state):
    mate_state = deepcopy(state)
    me = mate_state.player
    mate_state.set_player(mate_state.opponent)
    mate_state.set_opponent(me)

    opp_actions = find_actions(mate_state, mate_state.oppPieces)
    #print ("check mate test")
    #print ("# valid responses by opp:", len(opp_actions[0]))
    #for opm in opp_actions[0]:
        #print(opm.toString())
    if len(opp_actions[0]) == 0:
        return True

    return False

def check_castle(state,king):

    castle_moves = []

    k_side_cast = True
    q_side_cast = True

    #get castle info from fen
    if (state.fen_cast != None):
        k_side_cast = False
        q_side_cast = False
        if (state.player.color == "White"):
            if "K" in state.fen_cast:
                k_side_cast = True
            if "Q" in state.fen_cast:
                q_side_cast = True
        if (state.player.color == "Black"):
            if "k" in state.fen_cast:
                k_side_cast = True
            if "q" in state.fen_cast:
                q_side_cast = True

    # check board for castling
    if (king.moved == False):
        if (state.player.check == False):
            # check king side
            dirs = (1, -1)
            for dir in dirs:
                if(dir == 1 and k_side_cast == True) or (dir == -1 and q_side_cast == True):
                    check_r = king.rank
                    check_f1 = chr(ord(king.file) + 1 * dir)
                    check_f2 = chr(ord(king.file) + 2 * dir)
                    check_f3 = chr(ord(king.file) + 3 * dir)
                    if (dir == -1):
                        check_f4 = chr(ord(king.file) + 4 * dir)
                    key1 = coord_to_key(check_f1, check_r)
                    key2 = coord_to_key(check_f2, check_r)
                    key3 = coord_to_key(check_f3, check_r)
                    if (dir == -1):
                        key4 = coord_to_key(check_f4, check_r)
                    if (state.board.get(key1) == None):
                        if (state.board.get(key2) == None):
                            if (dir == 1):
                                rook_pls = state.board.get(key3)
                                if (rook_pls != None and rook_pls.type == "Rook" and rook_pls.moved == False):
                                    #if spaces aren't under attack
                                    fake_king1 = piece("King", check_f1, check_r, state.player, "99", False)
                                    space1_bad = in_check(state, fake_king1)
                                    fake_king2 = piece("King", check_f2, check_r, state.player, "100", False)
                                    space2_bad = in_check(state, fake_king2)
                                    if (space1_bad == False and space2_bad == False):
                                        # we can castle king side
                                        newMove = move(king, check_f2, check_r)
                                        castle_moves.append(newMove)
                            if (dir == -1):
                                if (state.board.get(key3) == None):
                                    rook_pls = state.board.get(key4)
                                    if (rook_pls != None and rook_pls.type == "Rook" and rook_pls.moved == False):
                                        fake_king1 = piece("King", check_f1, check_r, state.player, "99", False)
                                        space1_bad = in_check(state, fake_king1)
                                        fake_king2 = piece("King", check_f2, check_r, state.player, "100", False)
                                        space2_bad = in_check(state, fake_king2)
                                        fake_king3 = piece("King", check_f3, check_r, state.player, "101", False)
                                        space3_bad = in_check(state, fake_king3)
                                        if(space1_bad == False and space2_bad == False and space3_bad == False):
                                            # we can castle queen side
                                            newMove = move(king, check_f2, check_r)
                                            castle_moves.append(newMove)
    return castle_moves



def print_current_board(state):
    """Prints the current board using pretty ASCII art
    Note: you can delete this function if you wish
    """

    # iterate through the range in reverse order
    for r in range(9, -2, -1):
        output = ""
        if r == 9 or r == 0:
            # then the top or bottom of the board
            output = "   +------------------------+"
        elif r == -1:
            # then show the ranks
            output = "     a  b  c  d  e  f  g  h"
        else:  # board
            output = " " + str(r) + " |"
            # fill in all the files with pieces at the current rank
            allPieces = state.pieces
            allPieces += state.oppPieces
            for file_offset in range(0, 8):
                # start at a, with with file offset increasing the char
                f = chr(ord("a") + file_offset)
                current_piece = None
                for piece in allPieces:
                    if piece.file == f and piece.rank == r:
                        # then we found the piece at (file, rank)
                        current_piece = piece
                        break

                code = "."  # default "no piece"
                if current_piece:
                    # the code will be the first character of their type
                    # e.g. 'Q' for "Queen"
                    code = current_piece.type[0]

                    if current_piece.type == "Knight":
                        # 'K' is for "King", we use 'N' for "Knights"
                        code = "N"

                    if current_piece.owner.id == "1":
                        # the second player (black) is lower case.
                        # Otherwise it's uppercase already
                        code = code.lower()

                output += " " + code + " "

            output += "|"
        print(output)
