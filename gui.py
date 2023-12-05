import tkinter as tk
from tkinter import messagebox
from game import Game

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.selected_piece = None
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
        row, col = event.y // 80, event.x // 80
        if self.selected_piece:
            try:
                if self.game.make_move(self.selected_piece, (row, col)):
                    self.selected_piece = None
                    self.update_board()
                    if self.game.is_in_checkmate(self.game.current_turn):
                        messagebox.showinfo("Game Over", f"Checkmate! {self.game.current_turn.capitalize()} loses.")
                        self.root.quit()
                    return  # Exit the method after successful move
            except ValueError as e:
                messagebox.showerror("Invalid Move", str(e))
            # If move is unsuccessful or there's an error, reset selected piece
            self.selected_piece = None
        else:
            piece = self.game.board.board[row][col]
            if piece and piece.color == self.game.current_turn:
                self.selected_piece = (row, col)

    def update_board(self):
        self.draw_board()
        self.root.update()