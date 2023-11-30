class Piece:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def symbol(self):
        raise NotImplementedError

    def get_legal_moves(self, position, board):
        raise NotImplementedError


class Pawn(Piece):
    def symbol(self):
        return '♙' if self.color == 'white' else '♟'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Move forward
        if board.is_within_bounds(row + direction, col) and board.is_empty(row + direction, col):
            moves.append((row + direction, col))
            if row == start_row and board.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        # Captures
        for d_col in [-1, 1]:
            if board.is_within_bounds(row + direction, col + d_col) and board.is_opponent(row + direction, col + d_col, self.color):
                moves.append((row + direction, col + d_col))

        # En passant
        if board.en_passant_target:
            if board.en_passant_target == (row + direction, col + 1) or board.en_passant_target == (row + direction, col - 1):
                moves.append(board.en_passant_target)

        return moves


class Rook(Piece):
    def symbol(self):
        return '♖' if self.color == 'white' else '♜'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            while board.is_within_bounds(r, c) and board.is_empty(r, c):
                moves.append((r, c))
                r += d_row
                c += d_col
            if board.is_within_bounds(r, c) and board.is_opponent(r, c, self.color):
                moves.append((r, c))

        return moves


class Knight(Piece):
    def symbol(self):
        return '♘' if self.color == 'white' else '♞'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for d_row, d_col in offsets:
            r, c = row + d_row, col + d_col
            if board.is_within_bounds(r, c) and (board.is_empty(r, c) or board.is_opponent(r, c, self.color)):
                moves.append((r, c))

        return moves


class Bishop(Piece):
    def symbol(self):
        return '♗' if self.color == 'white' else '♝'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            while board.is_within_bounds(r, c) and board.is_empty(r, c):
                moves.append((r, c))
                r += d_row
                c += d_col
            if board.is_within_bounds(r, c) and board.is_opponent(r, c, self.color):
                moves.append((r, c))

        return moves


class Queen(Piece):
    def symbol(self):
        return '♕' if self.color == 'white' else '♛'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            while board.is_within_bounds(r, c) and board.is_empty(r, c):
                moves.append((r, c))
                r += d_row
                c += d_col
            if board.is_within_bounds(r, c) and board.is_opponent(r, c, self.color):
                moves.append((r, c))

        return moves


class King(Piece):
    def symbol(self):
        return '♔' if self.color == 'white' else '♚'

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            if board.is_within_bounds(r, c) and (board.is_empty(r, c) or board.is_opponent(r, c, self.color)):
                moves.append((r, c))

        # Castling moves
        if not self.has_moved:
            if self.color == 'white':
                back_row = 7
            else:
                back_row = 0

            # Kingside castling
            if board.is_empty(back_row, 5) and board.is_empty(back_row, 6):
                rook = board.board[back_row][7]
                if isinstance(rook, Rook) and not rook.has_moved and not board.is_under_attack((row, col), self.color):
                    if not board.is_under_attack((back_row, 5), self.color) and not board.is_under_attack((back_row, 6), self.color):
                        moves.append((back_row, 6))

            # Queenside castling
            if board.is_empty(back_row, 1) and board.is_empty(back_row, 2) and board.is_empty(back_row, 3):
                rook = board.board[back_row][0]
                if isinstance(rook, Rook) and not rook.has_moved and not board.is_under_attack((row, col), self.color):
                    if not board.is_under_attack((back_row, 2), self.color) and not board.is_under_attack((back_row, 3), self.color):
                        moves.append((back_row, 2))

        return moves
