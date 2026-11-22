# ============================================================
#  TIC-TAC-TOE with Intelligent Agent
#  Run this file directly: python tictactoe_play.py
# ============================================================

# ── Board Utilities ─────────────────────────────────────────

def display_board(board):
    print("+-------+-------+-------+")
    for row in range(3):
        print("|       |       |       |")
        for col in range(3):
            print("|   " + str(board[row][col]) + "   ", end="")
        print("|")
        print("|       |       |       |")
        print("+-------+-------+-------+")

def make_list_of_free_fields(board):
    return [(r, c) for r in range(3) for c in range(3)
            if board[r][c] not in ['O', 'X']]

def victory_for(board, sgn):
    who = 'me' if sgn == 'X' else 'you'
    for i in range(3):
        if all(board[i][c] == sgn for c in range(3)): return who
        if all(board[r][i] == sgn for r in range(3)): return who
    if all(board[i][i] == sgn for i in range(3)):     return who
    if all(board[i][2-i] == sgn for i in range(3)):   return who
    return None

def enter_move(board, symbol='O'):
    while True:
        move = input(f"  Enter your move (1-9): ")
        if len(move) == 1 and '1' <= move <= '9':
            move = int(move) - 1
            row, col = move // 3, move % 3
            if board[row][col] in ['O', 'X']:
                print("  That cell is already taken! Try again.")
            else:
                board[row][col] = symbol
                return board
        else:
            print("  Invalid input — enter a number from 1 to 9.")

def fresh_board():
    return [[3*j+i+1 for i in range(3)] for j in range(3)]


# ── Intelligent Agent ────────────────────────────────────────

class TicTacToeAgent:
    MY  = 'X'
    OPP = 'O'
    LINES   = [[(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
               [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
               [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)]]

    def _free(self, board):
        return make_list_of_free_fields(board)

    def _evaluate_line(self, vals):
        score = 0
        x_count = vals.count(self.MY)
        o_count = vals.count(self.OPP)
        empty_count = 3 - x_count - o_count

        if x_count == 3:
            score += 1000
        elif x_count == 2 and empty_count == 1:
            score += 10
        elif x_count == 1 and empty_count == 2:
            score += 1

        if o_count == 3:
            score -= 1000
        elif o_count == 2 and empty_count == 1:
            score -= 100  # High penalty for opponent having 2-in-a-row
        elif o_count == 1 and empty_count == 2:
            score -= 1
            
        return score

    def _evaluate_board(self, board):
        total_score = 0
        for line in self.LINES:
            vals = [board[r][c] for r, c in line]
            total_score += self._evaluate_line(vals)
        return total_score

    def perceive_and_act(self, board):
        free = self._free(board)
        if not free:
            return None

        best_score = -float('inf')
        best_move = None

        for r, c in free:
            original_val = board[r][c]
            # Simulate placing our symbol
            board[r][c] = self.MY
            
            # Evaluate the resulting board state mathematically
            score = self._evaluate_board(board)
            
            # Add a small positional bonus for center and corners
            if r == 1 and c == 1:
                score += 3
            elif (r, c) in [(0,0), (0,2), (2,0), (2,2)]:
                score += 2
                
            # Undo move
            board[r][c] = original_val

            # Choose the move that results in the highest board score
            if score > best_score:
                best_score = score
                best_move = (r, c)

        if best_move:
            print(f"  [Agent] Evaluated state utilities and chose square {best_move[0]*3+best_move[1]+1}")
            board[best_move[0]][best_move[1]] = self.MY
            return best_move


# ── Game Modes ───────────────────────────────────────────────

def play_human_vs_agent():
    board = fresh_board()
    agent = TicTacToeAgent()
    print("\n" + "="*35)
    print("   HUMAN  vs  COMPUTER (Agent)")
    print("   You = O  |  Computer = X")
    print("="*35)
    print("\n  Board positions:")
    display_board(board)

    # Agent always opens at center
    board[1][1] = 'X'
    print("  [Agent] Opening move: center (5)")
    display_board(board)

    human_turn = True
    while True:
        if human_turn:
            board = enter_move(board, 'O')
            victor = victory_for(board, 'O')
        else:
            agent.perceive_and_act(board)
            victor = victory_for(board, 'X')

        display_board(board)

        if victor == 'you':
            print("  🎉 You won! Congratulations!\n"); return
        elif victor == 'me':
            print("  🤖 Computer wins! Better luck next time.\n"); return
        elif not make_list_of_free_fields(board):
            print("  🤝 It's a tie!\n"); return

        human_turn = not human_turn


def play_human_vs_human():
    board = fresh_board()
    print("\n" + "="*35)
    print("     HUMAN  vs  HUMAN")
    print("   Player 1 = X  |  Player 2 = O")
    print("="*35)
    print("\n  Board positions:")
    display_board(board)

    p1_turn = True
    while True:
        if p1_turn:
            print("  Player 1 (X) — your turn")
            board = enter_move(board, 'X')
            victor = victory_for(board, 'X')
            winner_name = "Player 1 (X)"
        else:
            print("  Player 2 (O) — your turn")
            board = enter_move(board, 'O')
            victor = victory_for(board, 'O')
            winner_name = "Player 2 (O)"

        display_board(board)

        if victor:
            print(f"  🎉 {winner_name} wins!\n"); return
        elif not make_list_of_free_fields(board):
            print("  🤝 It's a tie!\n"); return

        p1_turn = not p1_turn


# ── Main Menu ────────────────────────────────────────────────

def main():
    while True:
        print("\n" + "="*35)
        print("    TIC-TAC-TOE  (Agent Edition)")
        print("="*35)
        print("  1. Human vs Computer (Agent)")
        print("  2. Human vs Human")
        print("  3. Quit")
        print("="*35)
        choice = input("  Select mode (1/2/3): ").strip()
        if   choice == '1': play_human_vs_agent()
        elif choice == '2': play_human_vs_human()
        elif choice == '3': print("  Goodbye! 👋\n"); break
        else: print("  Invalid choice — enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
