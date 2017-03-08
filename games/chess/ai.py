# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random
from games.chess.classes import state
from games.chess.classes import piece
from games.chess.classes import player
from games.chess.functions import find_actions
from games.chess.functions import result
from games.chess.functions import in_check

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

        print("me: ", me.id, "opp: ", opp.id)

        #me = player(self.player.in_check,self.player.rank_direction, self.player.name, self.player.id)
        #init state with current player
        #current_state = state(me)
        #read in starting board of game
        #need to check for castling and en passant of FEN string
        for p in self.game.pieces:
            new_p = piece(p.type, p.file, p.rank, p.owner, p.id, p.has_moved)
            current_state.addToBoard(new_p,new_p.key)

        #print(current_state.getPieces().get("a1").getType())

        # replace with your start logic

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



        # 4) make a valid, random move
        validMoves = find_actions(current_state,current_state.pieces)
        if(len(validMoves[0]) > 0):
            randMove = random.choice(validMoves[0])
            resultant_state = result(current_state, randMove)
            if (in_check(resultant_state)):
                print("this random move puts me in check!")
        else:
            randMove = None


        if(len(validMoves[0])==0):
            print("no valid moves to make")
            print("non check:", validMoves[0])
            print("everything:", end="")
            for mov in validMoves[1]:
                print(mov.toString())

        for x in (self.player.pieces):
            if x.id == randMove.piece.id:
                if(randMove.proType != None):
                    x.move(randMove.file, randMove.rank, randMove.proType)
                else:
                    x.move(randMove.file, randMove.rank)

        print("Random move made:", randMove.toString())
        print("All moves this piece could make:")
        for m in validMoves[0]:
            if randMove.piece.id == m.piece.id:
                print(self.player.color, m.toString(),end='.')
                print(" Piece id = ", m.piece.id)


        return True  # to signify we are done with our turn.

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
