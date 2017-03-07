# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random
from games.chess.state import state
from games.chess.state import piece
from games.chess.state import move
from games.chess.state import find_actions
from games.chess.state import player

current_state = (None)

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

        me = player(self.player.in_check,self.player.rank_direction, self.player.name, self.player.id)
        #init state with current player
        current_state = state(me)
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


        me = player(self.player.in_check, self.player.rank_direction, self.player.name, self.player.id)
        #read in player at start of turn, check for in check
        current_state = state(me)
        #read in game board pieces, add to state

        #reset game board
        current_state.resetState()

        #copy in board state to dictionary
        for p in self.game.pieces:
            new_p = piece(p.type, p.file, p.rank, p.owner, p.id, p.has_moved)
            current_state.addToBoard(new_p,new_p.key)

        #copy my own pieces to a list
        for p in self.player.pieces:
            my_p = piece(p.type, p.file, p.rank, p.owner, p.id, p.has_moved)
            current_state.addPieces(my_p)

        # 1) print the board to the console
        self.print_current_board()

        # 2) print the opponent's last move to the console
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random (and probably invalid) move.
        #random_piece = random.choice(self.player.pieces)
        # random_file = chr(ord("a") + random.randrange(8))
        # random_rank = random.randrange(8) + 1
        # random_piece.move(random_file, random_rank)

        validMoves = find_actions(current_state)
        randMove = random.choice(validMoves)

        if(len(validMoves)==0):
            print("no valid moves to make")

        '''
        goFile = randMove.file
        goRank = randMove.rank
        goProT = randMove.proType

        for x in (self.player.pieces):
            if x.type == "Knight":
                x.move(chr(ord(x.file) + 1), x.rank + self.player._rank_direction * 2)
                break
        '''

        for x in (self.player.pieces):
            if x.id == randMove.piece.id:
                if(randMove.proType != None):
                    x.move(randMove.file, randMove.rank, randMove.proType)
                else:
                    x.move(randMove.file, randMove.rank)

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
