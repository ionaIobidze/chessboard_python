from pieces import *


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.en_passant_target = None
        self.setup_board()

    def copy(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.en_passant_target = self.en_passant_target
        return new_board

    def setup_board(self):
        # Setup the board with all the pieces
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')

        self.board[0][0] = Rook('black')
        self.board[0][7] = Rook('black')
        self.board[7][0] = Rook('white')
        self.board[7][7] = Rook('white')

        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        self.board[7][1] = Knight('white')
        self.board[7][6] = Knight('white')

        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')
        self.board[7][2] = Bishop('white')
        self.board[7][5] = Bishop('white')

        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        # Setup kings
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        return self.board[row][col] is None

    def is_opponent(self, row, col, color):
        return self.board[row][col] is not None and self.board[row][col].color != color

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]
        if isinstance(piece, King) and abs(start[1] - end[1]) == 2:
            # taking care of the castling
            if end[1] == 6:  # Kingside castling
                self.board[start[0]][5] = self.board[start[0]][7]
                self.board[start[0]][7] = None
                self.board[start[0]][5].has_moved = True
            elif end[1] == 2:  # Queenside castling
                self.board[start[0]][3] = self.board[start[0]][0]
                self.board[start[0]][0] = None
                self.board[start[0]][3].has_moved = True

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None
        piece.has_moved = True

        # Handle en passant capture
        if isinstance(piece, Pawn) and end == self.en_passant_target:
            direction = 1 if piece.color == 'white' else -1
            self.board[end[0] - direction][end[1]] = None

        # Set en passant target
        if isinstance(piece, Pawn) and abs(start[0] - end[0]) == 2:
            self.en_passant_target = ((start[0] + end[0]) // 2, start[1])
        else:
            self.en_passant_target = None

        # Handle promotion
        if isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7):
            return True
        return False

    def is_under_attack(self, position, color):
        row, col = position
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is not None and piece.color != color:
                    if position in piece.get_legal_moves((r, c), self):
                        return True
        return False

    def is_in_check(self, color):
        king_position = self.find_king(color)
        return self.is_under_attack(king_position, color)

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if isinstance(piece, King) and piece.color == color:
                    return (r, c)
        return None
