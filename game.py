from board import Board
from pieces import Queen, Rook, Bishop, Knight


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'

    def is_move_legal(self, start, end):
        piece = self.board.board[start[0]][start[1]]
        if piece is None or piece.color != self.current_turn:
            return False

        legal_moves = piece.get_legal_moves(start, self.board)
        if end not in legal_moves:
            return False

        board_copy = self.board.copy()
        board_copy.move_piece(start, end)

        # Ensure the move is not leaving king with a check
        if board_copy.is_in_check(self.current_turn):
            return False

        return True

    def make_move(self, start, end):
        if self.is_move_legal(start, end):
            promotion_needed = self.board.move_piece(start, end)
            if promotion_needed:
                return 'promotion'
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        return False

    def promote_pawn(self, position, piece_type):
        row, col = position
        color = self.board.board[row][col].color

        if piece_type == 'Queen':
            self.board.board[row][col] = Queen(color)
        elif piece_type == 'Rook':
            self.board.board[row][col] = Rook(color)
        elif piece_type == 'Bishop':
            self.board.board[row][col] = Bishop(color)
        elif piece_type == 'Knight':
            self.board.board[row][col] = Knight(color)

    def is_in_check(self, color):
        return self.board.is_in_check(color)

    def is_in_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece is not None and piece.color == color:
                    for move in piece.get_legal_moves((row, col), self.board):
                        board_copy = self.board.copy()
                        board_copy.move_piece((row, col), move)
                        if not board_copy.is_in_check(color):
                            return False
        return True
