import tkinter as tk
from tkinter import messagebox
from game import Game


class ChessApp:
    def __init__(self, root):
        self.canvas = None
        self.root = root
        self.game = Game()
        self.selected_piece = None
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
            try:
                result = self.game.make_move(self.selected_piece, (row, col))
                if result == 'promotion':
                    self.show_promotion_dialog((row, col))
                else:
                    self.update_board()
                    if self.game.is_in_checkmate(self.game.current_turn):
                        messagebox.showinfo("Game Over", f"Checkmate! {self.game.current_turn.capitalize()} loses.")
                        self.root.quit()
                self.selected_piece = None
            except ValueError as e:
                messagebox.showerror("Invalid Move", str(e))
                self.selected_piece = None
        else:
            piece = self.game.board.board[row][col]
            if piece and piece.color == self.game.current_turn:
                self.selected_piece = (row, col)

    def update_board(self):
        self.draw_board()
        self.root.update()

    def show_promotion_dialog(self, position):
        self.promotion_window = tk.Frame(self.root, bg='white', bd=5)
        self.promotion_window.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def promote_to(piece_type):
            self.game.promote_pawn(position, piece_type)
            self.promotion_window.destroy()
            self.promotion_window = None
            self.update_board()
            self.end_turn()

        tk.Button(self.promotion_window, text="♕", command=lambda: promote_to('Queen')).pack()
        tk.Button(self.promotion_window, text="♖", command=lambda: promote_to('Rook')).pack()
        tk.Button(self.promotion_window, text="♗", command=lambda: promote_to('Bishop')).pack()
        tk.Button(self.promotion_window, text="♘", command=lambda: promote_to('Knight')).pack()

    def end_turn(self):
        self.game.current_turn = 'black' if self.game.current_turn == 'white' else 'white'
        if self.game.is_in_checkmate(self.game.current_turn):
            messagebox.showinfo("Game Over", f"Checkmate! {self.game.current_turn.capitalize()} loses.")
            self.root.quit()
