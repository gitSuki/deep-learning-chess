from enums import Team, Type
from gui import load_images

WHITE = Team.WHITE.value
BLACK = Team.BLACK.value

PAWN = Type.PAWN.value
ROOK = Type.ROOK.value
KNIGHT = Type.KNIGHT.value
BISHOP = Type.BISHOP.value
QUEEN = Type.QUEEN.value
KING = Type.KING.value

BOARD_SIZE = 512  # In pixels
GRID_DIMENSION = 8  # Amount of squares in each row and column
SQUARE_SIZE = BOARD_SIZE // GRID_DIMENSION  # The size of each square in pixels
FPS = 15
IMAGES = load_images(SQUARE_SIZE)
