import pyxel


class Score:

    def __init__(self):
        self.score = 0
        self.high_score = 0

    # Draws the score and the highscore #
    def draw(self):
        self.save_high_score()
        str_high_score = "Highscore: " + str(self.high_score)
        pyxel.text(200, 6, str(self.score), 7)
        pyxel.text(120, 6, str_high_score, 7)

    # Saves the last highscore of the same program #
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
