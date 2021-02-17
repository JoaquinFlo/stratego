BLUE: str = "blue"
RED: str = "red"


# CLASS THAT HOLDS VARIABLES PERTAINING TO CURRENT GAME STATE
class GameState:
    def __init__(self, colour: str, is_playing: bool, on_coord2: bool):
        self._colour = colour
        self._isPlaying = is_playing
        self._onCoord2 = on_coord2

    def get_colour(self) -> str:
        return self._colour

    def is_playing(self):
        return self._isPlaying

    def on_coord2(self):
        return self._onCoord2

    def set_is_playing(self, bool_value: bool):
        self._isPlaying = bool_value

    def set_on_coord2(self, bool_value: bool):
        self._onCoord2 = bool_value
