class Piece:
    # PIECE CONSTRUCTOR
    def __init__(self, rank: str, colour: str = None):
        self._rank = rank
        self._colour = colour

    # METHODS USED TO OBTAIN PIECE ATTRIBUTES
    def get_rank(self) -> str:
        return self._rank

    def get_colour(self) -> str:
        return self._colour
