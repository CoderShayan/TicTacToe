#----------------------------
#       Tic Tac Toe
#----------------------------

import tkinter as tk

import random

# Tic Tac Toe Game Class
class TicTacToe:

    # Initialize the game
    def __init__(self, root):
        
        self.root = root    # Initialize the main window    
        
        self.root.title("Tic Tac Toe")   # Set window title 
        
        self.root.geometry("375x500")   # Set window size (width x height)
        
        self.root.resizable(False, False)   # Disable window resizing
        
        self.root.configure(bg="#808080")  # Grey background

        # Header frame (main window, background color, height of the frame which is located at the top)
        self.header_frame = tk.Frame(self.root, bg="#808080", height=60)

        self.header_frame.pack(fill="x")    # Pack the header frame

        # Header label (title of the game in the header of the window)
        self.header_label = tk.Label(self.header_frame, text="Tic Tac Toe",
            font=("Arial", 28, "bold"), bg="#808080", fg="#101010")

        self.header_label.pack(pady=15) # Pack the header label and pady allow space around it

        self.mode = None    # Game mode ("1 vs 1" or "1 vs Bot") It will select by user

        self.current_player = "X"   # Current player ("X" or "O"), here "X" means player 1

        self.board = [[" " for _ in range(3)] for _ in range(3)]    # Game board (3x3 grid)

        # Button references for the game board
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Button references for the game board

        self.create_mode_selection()  # Create mode selection User Interface

        # Add result label at the bottom
        self.result_label = tk.Label(self.root,text="", font=("Arial", 20, "bold"),
                                    bg="#808080", fg="#39ff14")
        
        self.result_label.pack(side="bottom", pady=20) # Pack the result label on the bottom

        
    # Start the game with the selected mode
    def start_game(self, mode):

        self.mode = mode    # Set game mode which is "1 vs 1" or "1 vs Bot"
        self.mode_frame.destroy()   # Destroy mode selection frame
        self.create_board()  # Create game board

    def create_mode_selection(self):
        self.mode_frame = tk.Frame(self.root, bg="#808080")  # Grey background
        self.mode_frame.pack()
        tk.Label(self.mode_frame, text="Select Mode:", font=("Arial", 20), bg="#808080",
                 fg="black").pack(pady=10)
        tk.Button(self.mode_frame, text="1 vs 1", font=("Arial", 20), 
                  command=lambda: self.start_game("1")).pack(pady=10)
        tk.Button(self.mode_frame, text="1 vs Bot", font=("Arial", 20),
                  command=lambda: self.start_game("2")).pack(pady=10)

    def create_board(self):

        # Outer frame with thick border
        self.outer_frame = tk.Frame(self.root, bg="#808080",
            highlightbackground="#000000",  # Darkest black
            highlightthickness=5,           # Thick border
            bd=0
        )
        self.outer_frame.pack(pady=10)

        self.board_frame = tk.Frame(self.outer_frame, bg="#808080")
        self.board_frame.pack()

        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.board_frame, text=" ",
                        width=5, height=2, font=("Arial", 24),
                        bg="#000000", fg="#39ff14",
                        activebackground="#000000",
                        highlightbackground="#000000",  # Black border
                        highlightcolor="#39ff14",
                        highlightthickness=5,
                        bd=2,
                        command=lambda row=r, col=c: self.on_click(row, col)
                    )
                btn.grid(row=r, column=c, padx=0, pady=0)
                self.buttons[r][c] = btn
                
        # Add a thick bottom border
        self.bottom_border = tk.Frame(self.outer_frame, bg="#000000",
            height=18,   # Increase this value for thicker border
            width=1
        )
        self.bottom_border.pack(fill="x", side="bottom")
                
    def on_click(self, row, col):
        if self.board[row][col] != " ":
            return
        if self.mode == "1" or (self.mode == "2" and self.current_player == "X"):
            self.board[row][col] = self.current_player
            neon_color = "#39ff14" if self.current_player == "X" else "#ff073a"
            self.buttons[row][col].config(text=self.current_player, fg=neon_color)
            if self.check_win(self.current_player):
                self.end_game(f"Player {self.current_player} wins!")
                return
            if self.check_draw():
                self.end_game("It's a draw!")
                return
            self.current_player = "O" if self.current_player == "X" else "X"
            if self.mode == "2" and self.current_player == "O":
                self.root.after(400, self.bot_move)

    def bot_move(self):
        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        if not empty:
            return
        row, col = random.choice(empty)
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O", fg="#ff073a")  # Neon red for O
        if self.check_win("O"):
            self.end_game("Bot wins!")
            return
        if self.check_draw():
            self.end_game("It's a draw!")
            return
        self.current_player = "X"

    def check_win(self, player):
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]):
                return True
            if all([self.board[j][i] == player for j in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]):
            return True
        if all([self.board[i][2-i] == player for i in range(3)]):
            return True
        return False

    def check_draw(self):
        return all([cell != " " for row in self.board for cell in row])

    def end_game(self, msg):
        # Show result in the result label at the bottom
        self.result_label.config(text=msg)
        # Disable all buttons after game ends
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
