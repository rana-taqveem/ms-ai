import math
import time

class MathDuel:
    def __init__(self, start_number=10, allowed_moves=None):
        if allowed_moves is None:
            allowed_moves = [1, 2, 3]
        self.start_number = start_number
        self.allowed_moves = allowed_moves
        self.current_number = start_number
        self.player_turn = 1  # Player 1 starts (MAX)
        self.game_over = False
        self.winner = None
        self.move_history = []

    def reset(self):
        """Reset the game state."""
        self.current_number = self.start_number
        self.player_turn = 1
        self.game_over = False
        self.winner = None
        self.move_history = []

    def make_move(self, move):
        """TODO: Implement making a move.
        - Subtract `move` from current_number
        - Check if the game is over
        - Switch turns
        """

        self.current_number = self.current_number - move
        self.move_history.append(move)

        if self.current_number <= 0:
            self.game_over = True
            self.winner = self.player_turn
        else:
            if self.player_turn == 1:
                self.player_turn = 2
            else:
                self.player_turn = 1

    def evaluate(self, state, is_maximizing):
        """TODO: Implement evaluation function.
        Return:
          +1 if MAX wins
          -1 if MIN wins
           0 if game not over
        # """

        # we are returning 1 for inverse of Maximizing here becasue 
        # we got in this function call after the Max had already made the move in previous iteration and already own,
        #  but this call is for Min but Max won already, this it ture vice versa
        return 1 if not is_maximizing else -1
        
        
    def minimax(self, state, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        """TODO: Implement minimax with alpha-beta pruning.
        Arguments:
          - state: current number
          - depth: search depth
          - is_maximizing: True if MAX's turn, False if MIN's
        Return:
          Evaluation value for the state
        """

        best_move = None
        best_utility_value = None
        
        if state == 0:
            return self.evaluate(state, is_maximizing)

        for move in self.allowed_moves:
            new_state = state - move
            if new_state >= 0:
                if is_maximizing:
                    utility_value = self.minimax(new_state, depth + 1, False, alpha, beta)
                    if best_utility_value is None or utility_value > best_utility_value:
                        # update with new best utility value
                        best_utility_value = utility_value 

                        # record the best move for Max
                        best_move = move

                    # check for pruning for Max node 
                    # i.e. beta uptill now is samller then the current Max 
                    # then we can prune
                    if beta <= best_utility_value:
                        return best_utility_value
                
                    # we were no able to prune, so update alpha to best value if possible
                    if best_utility_value > alpha:
                        alpha = best_utility_value
                        
                else:
                    utility_value = self.minimax(new_state, depth + 1, True, alpha, beta)

                    # check if the new utility value is better than the previous values
                    # if yes then update the best utility value for min to lower value we just got
                    if best_utility_value is None or utility_value < best_utility_value:
                        best_utility_value = utility_value

                        # record the best move for Min
                        best_move = move

                    # Now we will check for pruning for Min Node
                    # i.e. if the alpha best utility value is less already less than the alpha values from children
                    # then we just prune
                    if  alpha >= best_utility_value:
                        return best_utility_value
                    
                    # we were
                    # not able to prune so we need to explore fruther
                    # update beta if the current best utility value is less than beta
                    if best_utility_value < beta:
                        beta = best_utility_value
    
        if depth == 0:
            self.best_move = best_move

        return best_utility_value


    def get_best_move(self):
        """TODO: Use minimax to find the best move for the current player."""

        is_maximizing = self.player_turn == 1
        self.minimax(self.current_number, 0, is_maximizing)

        return self.best_move

    def print_game_state(self):
        """Print the current state of the game."""
        player_name = "Player 1" if self.player_turn == 1 else "AI"
        role = "MAX" if self.player_turn == 1 else "MIN"
        print(f"\nCurrent number: {self.current_number}")
        print(f"{player_name}'s turn ({role})")
        print(f"Allowed moves: {[m for m in self.allowed_moves if m <= self.current_number]}")
        if self.game_over:
            print(f"Game over! {player_name} wins!")


