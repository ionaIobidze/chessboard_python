import tkinter as tk
from tkinter import messagebox
from game import Game


class ChessApp:
    def __init__(self, root):
        self.canvas = None
        self.root = root
        self.game = Game()
        self.selected_piece = None
        self.highlighted_squares = []
        self.promotion_window = None
        self.create_ui()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=640, height=640)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                if (row, col) in self.highlighted_squares:
                    color = '#FFD700'  # Highlight color for possible moves
                else:
                    color = '#40A578' if (row + col) % 2 == 0 else '#006769'
                self.canvas.create_rectangle(col * 80, row * 80, (col + 1) * 80, (row + 1) * 80, fill=color)
                piece = self.game.board.board[row][col]
                if piece is not None:
                    self.canvas.create_text(col * 80 + 40, row * 80 + 40, text=piece.symbol(), font=("Arial", 32))

    def on_click(self, event):
        if self.promotion_window is not None:
            return  # Ignore clicks when promotion window is open

        row, col = event.y // 80, event.x // 80
        if self.selected_piece:
            if (row, col) == self.selected_piece:
                # Deselect the piece
                self.selected_piece = None
                self.highlighted_squares = []
                self.draw_board()
                return

            result = self.game.make_move(self.selected_piece, (row, col))
            if result == 'promotion':
                self.show_promotion_dialog((row, col))
            else:
                self.update_board()
                if self.game.is_in_checkmate(self.game.current_turn):
                    self.show_game_over(f"Checkmate! {self.game.current_turn.capitalize()} loses.")
                self.selected_piece = None
                self.highlighted_squares = []
        else:
            piece = self.game.board.board[row][col]
            if piece and piece.color == self.game.current_turn:
                self.selected_piece = (row, col)
                self.highlighted_squares = piece.get_legal_moves((row, col), self.game.board)
                self.highlighted_squares.append((row, col))  # Highlight the selected piece
        self.draw_board()

    def update_board(self):
        self.draw_board()
        self.root.update()

    def show_promotion_dialog(self, position):
        self.promotion_window = tk.Toplevel(self.root)
        self.promotion_window.title("Pawn Promotion")
        self.promotion_window.geometry("200x200")
        self.promotion_window.transient(self.root)

        # Make sure the window is updated and viewable
        self.promotion_window.update_idletasks()
        self.promotion_window.grab_set()

        frame = tk.Frame(self.promotion_window, bg='white', bd=5)
        frame.pack(expand=True, fill=tk.BOTH)

        def promote_to(piece_type):
            self.game.promote_pawn(position, piece_type)
            self.promotion_window.destroy()
            self.promotion_window = None
            self.update_board()
            self.end_turn()

        button_font = ("Arial", 24)
        tk.Button(frame, text="♕", font=button_font, command=lambda: promote_to('Queen')).pack(fill=tk.BOTH,
                                                                                               expand=True)
        tk.Button(frame, text="♖", font=button_font, command=lambda: promote_to('Rook')).pack(fill=tk.BOTH, expand=True)
        tk.Button(frame, text="♗", font=button_font, command=lambda: promote_to('Bishop')).pack(fill=tk.BOTH,
                                                                                                expand=True)
        tk.Button(frame, text="♘", font=button_font, command=lambda: promote_to('Knight')).pack(fill=tk.BOTH,
                                                                                                expand=True)

    def show_game_over(self, message):
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")
        game_over_window.geometry("300x200")
        game_over_window.transient(self.root)

        # Make sure the window is updated and viewable
        game_over_window.update_idletasks()
        game_over_window.grab_set()

        frame = tk.Frame(game_over_window, bg='white', bd=5)
        frame.pack(expand=True, fill=tk.BOTH)

        label = tk.Label(frame, text=message, font=("Arial", 18), bg='white')
        label.pack(pady=20)

        def close_game():
            game_over_window.destroy()
            self.root.quit()

        button_font = ("Arial", 16)
        tk.Button(frame, text="OK", font=button_font, command=close_game).pack(pady=10)

    def end_turn(self):
        self.game.current_turn = 'black' if self.game.current_turn == 'white' else 'white'
        if self.game.is_in_checkmate(self.game.current_turn):
            self.show_game_over(f"Checkmate! {self.game.current_turn.capitalize()} loses.")
