import pyxel

from Sprites import Mario, Platform, Enemies, Coin, constants, Pow
from Collisions import Collisions
from Score import Score

Enemies = Enemies()
level = Platform(0, 0)
Mario1 = Mario()
Score1 = Score()
Coin1 = Coin()
Pow1 = Pow()

# Combines all classes #


class Main:
    def __init__(self):
        self.start = False

    def update(self):

        # After spacebar is pressed the game starts #
        if self.start:
            self.hit()
            Mario1.update()
            Coin1.update()

            if Pow1.is_alive:
                Pow1.update()

            # Updates each object in the lists #
            for i in range(len(Coin1.list_coins)):

                if Coin1.list_coins[i].is_alive:
                    Coin1.list_coins[i].update()

            # Deletes the objects in the lists #

            for j in range(len(Coin1.list_coins)):

                if not Coin1.list_coins[j - 1].is_alive and Coin1.list_coins[j - 1].frame_Sprite > 4:
                    del Coin1.list_coins[j - 1]

            Enemies.update()

            # Deletes the enemies and makes them fall down if they are dead #
            for k in range(len(Enemies.list_enemies)):

                if Enemies.list_enemies[k].is_alive:
                    Enemies.list_enemies[k].update()

                else:
                    Enemies.list_enemies[k].y += 7
                    Enemies.list_enemies[k].direct = "sleep"

            for u in range(len(Enemies.list_enemies)):

                if Enemies.list_enemies[u - 1].y > 256:
                    del Enemies.list_enemies[u - 1]

            # Establishes the characteristics of the levels #
            # as well as the collisions with the platforms #
            if Score1.score < 24000:
                Enemies.level = 0
                for t in range(len(Enemies.list_enemies)):
                    Enemies.list_enemies[t].level = 0
                Mario1.level = 0
                level.level = 0
                for u in range(len(Coin1.list_coins)):
                    Coin1.list_coins[u].level = 0

            elif 24000 <= Score1.score < 48000:
                Enemies.level = 1
                for t in range(len(Enemies.list_enemies)):
                    Enemies.list_enemies[t].level = 1
                Mario1.level = 1
                level.level = 1
                for u in range(len(Coin1.list_coins)):
                    Coin1.list_coins[u].level = 1

            elif 48000 <= Score1.score < 72000:
                Enemies.level = 2
                for t in range(len(Enemies.list_enemies)):
                    Enemies.list_enemies[t].level = 2
                Mario1.level = 2
                level.level = 2
                for u in range(len(Coin1.list_coins)):
                    Coin1.list_coins[u].level = 2

            elif Score1.score >= 72000:
                Enemies.level = 3
                for t in range(len(Enemies.list_enemies)):
                    Enemies.list_enemies[t].level = 3
                Mario1.level = 3
                level.level = 3
                for u in range(len(Coin1.list_coins)):
                    Coin1.list_coins[u].level = 3

        # If Mario dies, the game stops, characters stop moving #
        if not Mario1.is_alive:
            self.start = False

    def draw(self):

        # Initialize the game #
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start = True

        # Shows starting screen #
        if not pyxel.btnp(pyxel.KEY_SPACE) and not self.start and Mario1.is_alive:
            pyxel.blt(0, 0, 1, 0, 0, 256, 256, 0)
            pyxel.text(86, 200, "Press Space to start", 7)

        # Starts drawing the sprites #
        if self.start or not Mario1.is_alive:
            level.draw()

            if Pow1.is_alive:
                Pow1.draw()

            # Shows Mario when he is not affected by the enemies #
            if Mario1.inv_frames == 0 or Mario1.inv_frames % 2 == 0:
                Mario1.draw()

            # Draws each object of the lists #
            for i in range(len(Coin1.list_coins)):
                Coin1.list_coins[i].draw()

            for j in range(len(Enemies.list_enemies)):
                Enemies.list_enemies[j].draw()
            Score1.draw()

            # Stops the game and makes animation of Mario falling #

            if not Mario1.is_alive:
                pyxel.text(110, 200, "Game Over", 7)
                pyxel.text(86, 210, "Press Space to restart", 7)
                Mario1.draw()

                if Mario1.height_diff < 40:
                    Mario1.y -= 5
                    Mario1.height_diff += 5

                if Mario1.y < 256 and Mario1.height_diff == 40:
                    Mario1.y += 5

                if pyxel.btnp(pyxel.KEY_SPACE):
                    Mario1.lives = 3
                    Mario1.x = constants.x
                    Mario1.y = constants.y
                    Enemies.list_enemies.clear()
                    Coin1.list_coins.clear()
                    Score1.score = 0
                    Pow1.change = 0

    def hit(self):

        # Interactions between the sprites #
        col = Collisions(Mario1.x, Mario1.y, Mario1.level)
        col.detect_collision_player()
        for i in range(len(Enemies.list_enemies)):
            for j in range(-16, 16):

                # If you jump while below the block of the enemy, it goes to sleep #
                if (Mario1.x + j == Enemies.list_enemies[i].x and
                        Mario1.y - 21 == Enemies.list_enemies[i].y and
                        col.col_up):
                    Enemies.list_enemies[i].is_sleep = True

                # If you kick the enemy while asleep, it dies #

                if (Mario1.x + j == Enemies.list_enemies[i].x and
                        Mario1.y + 9 == Enemies.list_enemies[i].y and
                        Enemies.list_enemies[i].is_sleep):
                    Enemies.list_enemies[i].is_alive = False

                    if Enemies.list_enemies[i].change == 0:
                        Score1.score += 800

                    else:
                        Score1.score += 1600

                # inv_frames was added not to die instantly in contact #
                if (Mario1.x + j == Enemies.list_enemies[i].x and
                        Mario1.y + 9 == Enemies.list_enemies[i].y and
                        not Enemies.list_enemies[i].is_sleep and
                        Mario1.inv_frames == 0):
                    Mario1.lives -= 1
                    Mario1.inv_frames = 60

                # Contact between the enemies #
                for t in range(len(Enemies.list_enemies) - 1):

                    if (Enemies.list_enemies[i].x + j == Enemies.list_enemies[t].x and
                            Enemies.list_enemies[i].y == Enemies.list_enemies[t].y):

                        if Enemies.list_enemies[i].direct == "right":
                            Enemies.list_enemies[i].direct = "left"
                            Enemies.list_enemies[i].x -= 2
                            Enemies.list_enemies[t].direct = "right"
                            Enemies.list_enemies[t].x += 2

                        else:
                            Enemies.list_enemies[i].direct = "right"
                            Enemies.list_enemies[i].x += 2
                            Enemies.list_enemies[t].direct = "left"
                            Enemies.list_enemies[t].x -= 2

        # Interaction between coin and Mario #
        for c in range(len(Coin1.list_coins)):
            for d in range(-16, 16):

                if (Mario1.x + d == Coin1.list_coins[c].x and
                        Mario1.y + 9 == Coin1.list_coins[c].y and
                        Coin1.list_coins[c].is_alive):
                    Score1.score += 800
                    Coin1.list_coins[c].is_alive = False

        # Interaction between Mario and Pow #
        for f in range(-8, 8):
            if (Mario1.x + f == Pow1.x and
                    Mario1.y <= 41 and Pow1.is_alive
                    and Mario1.jump):
                Mario1.jump = False
                Mario1.height_diff = 75
                Mario1.jump_speed = 5
                Pow1.change += 1
                for i in range(len(Enemies.list_enemies)):

                    if not Enemies.list_enemies[i].fall and not Enemies.list_enemies[i].jump:
                        Enemies.list_enemies[i].is_sleep = True


Main = Main()
