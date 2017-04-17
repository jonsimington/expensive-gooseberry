# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random
from operator import attrgetter
from games.chess.classes import state
from games.chess.classes import piece
from games.chess.classes import player
from games.chess.functions import find_actions
from games.chess.functions import result
from games.chess.functions import in_check
from games.chess.functions import check_mate
from games.chess.functions import copy_state
import time


current_state = (None)
fen = None

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "The Wildcats! feat. Wallace James Haviland III"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """

        fen = self.game.fen

        castling = fen[2]
        enPass = fen[3]

        for playa in self.game.players:
            if playa.id == self.player.id:
                me = player(playa.in_check, playa.rank_direction, playa.name, playa.id, playa.color)
            else:
                opp = player(playa.in_check, playa.rank_direction, playa.name, playa.id, playa.color)

        current_state = state(me, opp, self.player.id)
        current_state.add_init_fen(fen)
        print("fen cast = ", current_state.fen_cast)

        print("me: ", me.toString(), "opp: ", opp.toString())

        #init state with current player
        #read in starting board of game
        #need to check for castling and en passant of FEN string
        for p in self.game.pieces:
            new_p = piece(p.type, p.file, p.rank, p.owner, p.id, p.has_moved)
            current_state.addToBoard(new_p,new_p.key)

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """

        # replace with your game updated logic

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
        dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or
                          lost.
        """

        # replace with your end logic

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your
                  turn, False means to keep your turn going and re-call this
                  function.
        """

        # Here is where you'll want to code your AI.

        for playa in self.game.players:
            if playa.id == self.player.id:
                me = player(playa.in_check, playa.rank_direction, playa.name, playa.id, playa.color)
            else:
                opp = player(playa.in_check, playa.rank_direction, playa.name, playa.id, playa.color)

        current_state = state(me, opp, self.player.id)

        #reset game board
        current_state.resetState()


        #copy in board state to dictionary and pieces lists
        for p in self.game.pieces:
            new_p = piece(p.type, p.file, p.rank, p.owner, p.id, p.has_moved)
            current_state.addToBoard(new_p,new_p.key)
            if (p.owner.id == self.player.id):
                current_state.addPieces(new_p)
            else:
                current_state.addOppPiece(new_p)


        if(len(self.game.moves) <= 1):
            #game just started, check for fen
            fen = self.game.fen
            if fen != None:
                current_state.add_init_fen(fen)


        # 1) print the board to the console
        self.print_current_board()

        # 2) print the opponent's last move to the console AND copy to state to check en passant
        if len(self.game.moves) > 0:
            current_state.set_last_move(self.game.moves[-1].san)
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")


        # 3.5) Clear history table every 10 moves
        if len(self.game.moves) % 10 == 0:
            self.clear_history_table()


        # 4) find best move w/ DLM
        time_limit = 2
        start = time.time()
        next_move = self.IDM(current_state, start, time_limit)

        print("move made:", next_move.toString())

        for x in (self.player.pieces):
            if x.id == next_move.piece.id:
                if(next_move.proType != None):
                    x.move(next_move.file, next_move.rank, next_move.proType)
                else:
                    x.move(next_move.file, next_move.rank)

        return True  # to signify we are done with our turn.


    _history_table = {}

    @property
    def history_table(self):
        return self._history_table

    def get_HT_val(self, board):
        return self._history_table.get(hash(frozenset(board)))

    def clear_history_table(self):
        self._history_table = {}

    def add_to_HT(self, board, val):
        key = hash(frozenset(board))
        self._history_table[key] = val

    def increase_HT_val(self, board):
        key = hash(frozenset(board))
        temp = self._history_table.get(key)
        temp += 1
        self.add_to_HT(board,temp)

    def IDM(self, state, start_time, time_limit):
            # check time
        now = time.time()
        diff = 0
        limit = 0
        best_act = None
        while(diff < time_limit):
            limit += 1
            alpha = None
            beta = None
            q_limit = 2
            print("dlm called with lim = " + str(limit), end=" ")
            best_act = self.DLM(state, limit, q_limit, alpha, beta)
            now = time.time()
            diff = now - start_time
            print(" - complete. time elapsed = " + str(diff))

        print("time up, diff = " + str(diff) + " max was " + str(time_limit))
        return best_act

    def DLM(self, state, limit, q_limit, alpha, beta):
        print("DLM - player at move: " + state.player.toString() + " limit = " + str(limit))
        actions = find_actions(state, state.pieces)
        frontier = []
        for action in actions[0]:
            child = result(state, action)
            child_eval = self.MinV(child, limit - 1, q_limit, alpha, beta)
            child.set_state_eval(child_eval)

            if not alpha or child_eval > alpha:
                alpha = child_eval

            frontier.append(child)
        random.shuffle(frontier)

        best_state = max(frontier, key=attrgetter('state_eval'))
        if not self.get_HT_val(best_state.board):
            self.add_to_HT(best_state.board, 1)
        else:
            self.increase_HT_val(best_state.board)
        print("best action chose eval = ", best_state.state_eval)
        return best_state.last_move



    def MaxV(self, parent, limit, q_limit, alpha, beta):
        #do MaxV
        #print("MaxV - player at move: " + parent.player.toString())
        #only continue if quiesant search or lim not reached
        if limit > 0 or (not parent.quiesant and q_limit > 0):
            max_state = copy_state(parent, True)
            term = self.terminal_test(max_state)
            if not term:
                parent_eval = self.calc_state_eval(parent)
                actions = find_actions(max_state, max_state.pieces)
                frontier = []
                for action in actions[0]:
                    child = result(max_state, action)
                    #check if board in history table to sort frontier
                    if self.get_HT_val(child.board):
                        child.set_his_val(self.get_HT_val(child.board))
                    frontier.append(child)
                sorted(frontier, key=attrgetter('history_table_val'))
                for child in frontier:
                    if child.player_in_check:
                        child.set_quiesant(False)
                    if self.calc_state_eval(child) != parent_eval:
                        child.set_quiesant(False)
                    if limit == 0:
                        #then quiesant search
                        new_q_lim = q_limit
                        q_limit -= 1
                    child_eval = self.MinV(child, limit-1, q_limit, alpha, beta)
                    child.set_state_eval(child_eval)
                    if not alpha or child_eval > alpha:
                        alpha = child_eval
                    if beta and child_eval > beta:  #failhigh on prune
                        #print("prune!")
                        if not self.get_HT_val(child.board):
                            self.add_to_HT(child.board, 1)
                        else:
                            self.increase_HT_val(child.board)
                        return child_eval
                max_state = max(frontier, key = attrgetter('state_eval'))
                if not self.get_HT_val(max_state.board):
                    self.add_to_HT(max_state.board, 1)
                else:
                    self.increase_HT_val(max_state.board)
                return max_state.state_eval
            elif term == "Mate":
                return 1000
            elif term == "Stalemate" or term == "Draw":
                return self.calc_state_eval(parent)
            else:
                print("Error, terminal test returned invalid value")

        else:
            return self.calc_state_eval(parent)

    def MinV(self, parent, limit, q_limit, alpha, beta):
        # do MinV
        #print("MinV - player at move: " + parent.player.toString())
        if limit > 0 or (not parent.quiesant and q_limit > 0):
            min_state = copy_state(parent, True)
            term = self.terminal_test(min_state)
            if not term:
                parent_eval = self.calc_state_eval(parent)
                actions = find_actions(min_state, min_state.pieces)
                frontier = []
                for action in actions[0]:
                    child = result(min_state, action)
                    #check if board in history table to sort frontier
                    if self.get_HT_val(child.board):
                        child.set_his_val(self.get_HT_val(child.board))
                    frontier.append(child)
                sorted(frontier, key=attrgetter('history_table_val'))
                for child in frontier:
                    if child.player_in_check:
                        child.set_quiesant(False)
                    if self.calc_state_eval(child) != parent_eval:
                        child.set_quiesant(False)
                    if limit == 0:
                        #then quiesant search
                        new_q_lim = q_limit
                        q_limit -= 1
                    child_eval = self.MaxV(child, limit - 1, q_limit, alpha, beta)
                    child.set_state_eval(child_eval)
                    if not beta or child_eval < beta:
                         beta = child_eval
                    if alpha and child_eval < alpha:
                        #print("prune!")
                        if not self.get_HT_val(child.board):
                            self.add_to_HT(child.board, 1)
                        else:
                            self.increase_HT_val(child.board)
                        return child_eval
                min_state = min(frontier, key=attrgetter('state_eval'))
                if not self.get_HT_val(min_state.board):
                    self.add_to_HT(min_state.board, 1)
                else:
                    self.increase_HT_val(min_state.board)
                return min_state.state_eval
            elif term == "Mate":
                return -1000
            elif term == "Stalemate" or term == "Draw":
                return self.calc_state_eval(parent)
            else:
                print("Error, terminal test returned invalid value")
        else:
            return self.calc_state_eval(parent)


    def calc_state_eval(self, eval_state):
        calc = 0
        all_pieces = eval_state.pieces + eval_state.oppPieces
        for p in all_pieces:
            if p.owner.id == self.player.id:
                calc += piece_val(p)
            else:
                calc -= piece_val(p)

        return calc

    def terminal_test(self, term_state):
        mate = check_mate(term_state)
        if term_state.player.check == True and mate == True:
            print("terminal test: Mate found")
            return "Mate"
        if term_state.player.check == False and mate == True:
            print("terminal test: Stalemate found")
            return "Stalemate"
        all_pieces = term_state.pieces + term_state.oppPieces
        if len(all_pieces) <= 3:
            for p in all_pieces:
                if p.type != "King" or p.type != "Bishop" or p.type != "Knight":
                    return False
            print("terminal test: Draw found")
            return "Draw"
        return False

    def print_current_board(self):
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
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
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

def piece_val(piece):
    if piece.type == "Pawn":
        return 1
    if piece.type == "Bishop" or piece.type == "Knight":
        return 3
    if piece.type == "Rook":
        return 5
    if piece.type == "Queen":
        return 9
    return 0