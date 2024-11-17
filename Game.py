import pyxel
from Main import Main
from Constants import Constants
constants = Constants()


# The values that can be changed are in constants #
# Starts the program #
# The game is infinite and the objective is to get the highest score possible #
class Game:

    def __init__(self):
        pyxel.init(constants.game_width, constants.game_height, title="Mario", fps=30)
        pyxel.load("assets\sprites-aci-lib.pyxres")
        pyxel.run(Main.update, Main.draw)


Game()
