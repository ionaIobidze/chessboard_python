from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'

    def is_move_legal(self, start, end):
        piece = self.board.board[start[0]][start[1]]
        if piece is None or piece.color != self.current_turn:
            return False
        return end in piece.get_legal_moves(start, self.board)

    def make_move(self, start, end):
        if self.is_move_legal(start, end):
            self.board.move_piece(start, end)
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        return False

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
