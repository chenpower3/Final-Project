import pyxel
import random
from Constants import Constants
from Collisions import Collisions

constants = Constants()


# Common mother class for Mario, Enemy and Platform #
class Sprite:
    # Initialize the common constants between Mario, Enemy and Platform #

    def __init__(self):
        self.x = constants.x
        self.y = constants.y
        self.direct = "right"
        self.frame_Sprite = 0
        self.fall = False
        self.jump_speed = 10
        self.is_alive = True
        self.jump = False
        self.height_diff = 0
        self.change = 0
        self.level = 0
        self.list_coins = []

    # Creating setters for the common attributes #
    # Check that the x and y positions are integers and allow them to be changed #
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x: int or float):
        if not isinstance(x, int) and not isinstance(x, float):
            raise TypeError("x must be an int or a float")
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y: int or float):

        if not isinstance(y, int) and not isinstance(y, float):
            raise TypeError("y must be a float or and int")

        else:
            self.__y = y

    @property
    def direct(self):
        return self.__direct

    @direct.setter
    def direct(self, direct: str):

        if not isinstance(direct, str):
            raise TypeError("direct must be a str")

        if direct != "right" and direct != "left" and direct != "sleep":
            raise ValueError("direct must be left, right or sleep")

        else:
            self.__direct = direct


# This class will create the playable character Mario and uses inheritance#
class Mario(Sprite):

    def __init__(self):
        self.lives = constants.lives
        self.inv_frames = 0
        super().__init__()

    # This function executes each jump #
    def update(self):
        self.move()
        if self.frame_Sprite > 2:
            self.frame_Sprite = 0

        if self.inv_frames > 0:
            self.inv_frames -= 1

        if self.lives <= 0:
            self.is_alive = False
            self.height_diff = 0

        else:
            self.is_alive = True

    # This function creates the character and is executed each frame #
    def draw(self):
        for i in range(self.lives):
            pyxel.blt(30 + 8 * i, 6, 0, 8, 0, 8, 8, 0)

        if self.is_alive:

            if self.direct == "right":

                if self.height_diff == 0:
                    pyxel.blt(self.x, self.y, 0, constants.u[self.frame_Sprite], 7,
                              constants.player_w_right[self.frame_Sprite], constants.player_h,
                              0)

                else:
                    pyxel.blt(self.x, self.y, 0, 64, 8, 14, constants.player_h, 0)

            if self.direct == "left":

                if self.height_diff == 0:
                    pyxel.blt(self.x, self.y, 0, constants.u[self.frame_Sprite], 7,
                              constants.player_w_left[self.frame_Sprite], constants.player_h,
                              0)

                else:
                    pyxel.blt(self.x, self.y, 0, 64, 8, -14, constants.player_h, 0)

        elif not self.is_alive:
            pyxel.blt(self.x, self.y, 0, 128, 8, 14, constants.player_h, 0)

    # This function checks if Mario is moving and changes its position if #
    # the movement keys are pressed #

    def move(self):
        col = Collisions(self.x, self.y, self.level)
        col.detect_collision_player()

        # Makes Mario go to the left and changes its sprite #
        if pyxel.btn(pyxel.KEY_LEFT):

            if self.height_diff == 0 or self.jump or self.fall:
                self.direct = "left"

                if not col.col_left:
                    self.x -= constants.dx

                if pyxel.frame_count % 1.5 == 0:
                    self.frame_Sprite += 1

        # Makes Mario go to the right and changes its sprite #
        if pyxel.btn(pyxel.KEY_RIGHT):

            if self.height_diff == 0 or self.jump or self.fall:
                self.direct = "right"

                if not col.col_right:
                    self.x += constants.dx

                if pyxel.frame_count % 1.5 == 0:
                    self.frame_Sprite += 1

        if pyxel.btn(pyxel.KEY_LEFT) and pyxel.btn(pyxel.KEY_RIGHT):
            self.frame_Sprite = 0

        # To land with the default sprite #
        if not pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_LEFT):
            self.frame_Sprite = 0

        # It makes Mario jump if the up arrow is pressed #
        if pyxel.btn(pyxel.KEY_UP):

            if not self.jump and not self.fall and self.height_diff == 0:
                self.jump = True
                self.jump_speed = 10

        if col.col_up:
            self.height_diff = 75
            self.y += self.jump_speed

        # As long as jump is True, and we have not jumped 75 pixels it will go up #
        if self.jump:
            self.y -= self.jump_speed
            self.height_diff += self.jump_speed

            if self.jump_speed >= 5:
                self.jump_speed -= 1

            if self.height_diff >= 75:
                self.height_diff = 75
                self.jump = False

        if self.x >= 256 - 8:
            self.x = 0

        elif self.x <= - 8:
            self.x = 256 - 9

        # Starts the fall as long as there is no collision and it's not jumping #
        if not self.jump and not col.col_down:
            self.fall = True
            self.height_diff = 75

        # Defines the fall #
        if self.fall:

            if col.col_down:
                self.fall = False
                self.y = col.y_tile * 8

                if not self.jump:
                    self.height_diff = 0

            else:
                self.y += self.jump_speed

                # Establish a max speed #
                if self.jump_speed < 7:
                    self.jump_speed += 1


class Platform(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    # Draws the tile of the platforms #

    def draw(self):
        col = Collisions(self.x, self.y, self.level)
        col.detect_collision_player()
        pyxel.bltm(0, 0, self.level, self.x, self.y, 256, 256)


class Enemies(Sprite):

    def __init__(self):
        super().__init__()
        self.death_counter = 0
        self.spawn = random.randint(0, 1)
        self.list_enemies = []
        self.is_sleep = False
        self.dx = 1
        self.sleep_counter = 0
        self.y = 16
        self.death_counter = 0

        if self.spawn == 1:
            self.x = 218
            self.direct = "left"

        else:
            self.x = 24
            self.direct = "right"

    # Updates the enemy list and the sprites #
    def update(self):
        self.enemy_list()

        for i in range(len(self.list_enemies)):

            if pyxel.frame_count % 3 == 0:
                self.list_enemies[i].frame_Sprite += 1

    # Creates and appends the enemy to the list depending on time and level #
    def enemy_list(self):

        if pyxel.frame_count % 150 == 0 and self.level == 0 or self.level == 3:
            Enemy1 = Turtle()
            self.list_enemies.append(Enemy1)

        if pyxel.frame_count % 250 == 0 and self.level == 1 or self.level == 3:
            Enemy2 = Crab()
            self.list_enemies.append(Enemy2)

        if pyxel.frame_count % 500 == 0 and self.level == 2 or self.level == 3:
            Enemy3 = Monkey()
            self.list_enemies.append(Enemy3)


class Turtle(Enemies):

    def __init__(self):
        super().__init__()

    # Updates the position of the enemy, it is very similar in all the enemies but #
    # with little differences #
    def update(self):

        if not self.is_sleep:
            self.move()

        if self.direct != "left" and self.direct != "right" and not self.is_sleep:
            self.spawn = random.randint(0, 1)

            if self.spawn == 1:
                self.direct = "left"

            else:
                self.direct = "right"

        elif self.is_sleep:
            self.direct = "sleep"

            if self.is_alive:
                self.sleep_counter += 1

                if self.sleep_counter % 60 == 0:
                    self.is_sleep = False
                    self.dx = 2
                    self.change += 1

    # Draws the sprites of the enemies, changes depending on the characteristics of the enemy #
    def draw(self):

        if self.frame_Sprite > 2:
            self.frame_Sprite = 0

        # Normal sprite #
        if self.change == 0:

            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                          32, constants.en_w_right, 16, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                          32, constants.en_w_left, 16, 0)

            else:
                pyxel.blt(self.x, self.y, 0, constants.en_sleep[self.frame_Sprite - 1],
                          32, constants.en_w_left, 16, 0)

        else:

            # Changes sprite color #
            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.en_u2[self.frame_Sprite],
                          32, constants.en_w_right, 16, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.en_u2[self.frame_Sprite],
                          32, constants.en_w_left, 16, 0)

            else:
                pyxel.blt(self.x, self.y, 0, constants.en_sleep2[self.frame_Sprite - 1],
                          32, constants.en_w_left, 16, 0)

    # Describes the movement of the sprite, changes depending on the enemy #
    def move(self):
        col_en = Collisions(self.x, self.y, self.level)
        col_en.detect_collision_en()

        if self.direct == "right":
            self.x += self.dx

            if self.x >= 256 - 8:
                self.direct = "left"

        elif self.direct == "left":
            self.x -= self.dx

            if self.x <= - 8:
                self.direct = "right"

        if col_en.col_down:
            self.fall = False
            self.y = col_en.y_tile * 8 + 1

        else:
            self.fall = True

        if self.fall:
            self.jump_speed = 5
            self.y += self.jump_speed

            # Establish a max speed #
            if self.jump_speed < 7:
                self.jump_speed += 1

        if self.y == 233 and self.x <= 24:
            self.y = 0
            self.direct = "right"

        if self.y == 233 and self.x >= 218:
            self.y = 0
            self.direct = "left"


class Crab(Enemies):

    def __init__(self):
        super().__init__()
        self.hit_counter = 0

    def update(self):

        if not self.is_sleep:
            self.move()

        if self.direct != "left" and self.direct != "right" and not self.is_sleep:
            self.spawn = random.randint(0, 1)

            if self.spawn == 1:
                self.direct = "left"

            else:
                self.direct = "right"

        elif self.is_sleep:

            if self.hit_counter < 1:
                self.is_sleep = False
                self.hit_counter += 1

            else:
                self.direct = "sleep"

                if self.is_alive:

                    self.sleep_counter += 1

                    if self.sleep_counter % 60 == 0:
                        self.is_sleep = False
                        self.dx = 2
                        self.change += 1
                        self.hit_counter = 0

    def draw(self):

        if self.frame_Sprite > 2:
            self.frame_Sprite = 0

        if self.change == 0:

            if self.hit_counter == 1 and self.direct != "sleep":
                pyxel.rect(self.x, self.y, 4, 2, 7)

            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                          48, constants.en_w_right, 16, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                          48, constants.en_w_left, 16, 0)

            else:
                pyxel.blt(self.x, self.y, 0, constants.en_sleep[self.frame_Sprite - 1] + 16,
                          48, constants.en_w_left, 16, 0)

        else:

            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.en_u2[self.frame_Sprite],
                          48, constants.en_w_right, 16, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.en_u2[self.frame_Sprite],
                          48, constants.en_w_left, 16, 0)

            else:
                pyxel.blt(self.x, self.y, 0, constants.en_sleep2[self.frame_Sprite - 1] + 32,
                          48, constants.en_w_left, 16, 0)

    def move(self):
        col_en = Collisions(self.x, self.y, self.level)
        col_en.detect_collision_en()

        if self.direct == "right":
            self.x += self.dx

            if self.x >= 256 - 8:
                self.direct = "left"

        elif self.direct == "left":
            self.x -= self.dx

            if self.x <= - 8:
                self.direct = "right"

        if col_en.col_down:
            self.fall = False
            self.y = col_en.y_tile * 8 + 1

        else:
            self.fall = True

        if self.fall:
            self.jump_speed = 5
            self.y += self.jump_speed

            # Establish a max speed #
            if self.jump_speed < 7:
                self.jump_speed += 1

        if self.y == 233 and self.x <= 24:
            self.y = 16
            self.direct = "right"

        if self.y == 233 and self.x >= 218:
            self.y = 16
            self.direct = "left"


class Monkey(Enemies):

    def __init__(self):
        super().__init__()
        self.delay = 0

    def update(self):

        if not self.is_sleep:
            self.move()

        if self.direct != "left" and self.direct != "right" and not self.is_sleep:
            self.spawn = random.randint(0, 1)

            if self.spawn == 1:
                self.direct = "left"

            else:
                self.direct = "right"

        elif self.is_sleep:

            self.direct = "sleep"

            if self.is_alive:

                self.sleep_counter += 1

                if self.sleep_counter % 60 == 0:
                    self.is_sleep = False
                    self.dx = 2

    def draw(self):

        if self.frame_Sprite > 2:
            self.frame_Sprite = 0

        if self.direct == "right":
            pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                      64, constants.en_w_right, 16, 0)

        elif self.direct == "left":
            pyxel.blt(self.x, self.y, 0, constants.en_u[self.frame_Sprite],
                      64, constants.en_w_left, 16, 0)

        else:
            pyxel.blt(self.x, self.y, 0, constants.en_sleep[self.frame_Sprite - 1],
                      64, constants.en_w_left, 16, 0)

    def move(self):
        col_en = Collisions(self.x, self.y, self.level)
        col_en.detect_collision_en()

        if self.direct == "right":
            self.x += self.dx

            if self.x >= 256 - 8:
                self.direct = "left"

        elif self.direct == "left":
            self.x -= self.dx

            if self.x <= - 8:
                self.direct = "right"

        # Fall if there is no platform and jumps with a delay of 2 secs #

        if not col_en.col_down and not self.jump:
            self.fall = True

        if col_en.col_down:
            self.fall = False
            self.y = col_en.y_tile * 8 + 1

            if not self.is_sleep and not self.jump:
                self.delay += 1
                self.height_diff = 0

                if self.delay == 60:
                    self.jump = True
                    self.delay = 0

        if self.jump:
            self.y -= self.jump_speed
            self.height_diff += self.jump_speed

            if self.height_diff >= 35:
                self.height_diff = 35
                self.jump = False

        if self.fall:
            self.jump_speed = 3
            if not self.jump:
                self.y += self.jump_speed

            if self.jump_speed < 7:
                self.jump_speed += 1

        if self.y == 233 and self.x <= 24:
            self.y = 16
            self.direct = "right"

        if self.y == 233 and self.x >= 218:
            self.y = 16
            self.direct = "left"


class Coin(Sprite):

    def __init__(self):
        super().__init__()
        self.y = 16
        self.spawn = random.randint(0, 1)
        self.list_coins = []
        if self.spawn == 1:
            self.x = 218
            self.direct = "left"

        else:
            self.x = 24
            self.direct = "right"

    def draw(self):

        # Draws the coin if it is not dead, also changes sprites #
        if self.frame_Sprite > 4:
            self.frame_Sprite = 0

        if self.is_alive:

            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.coin_u[self.frame_Sprite],
                          94, constants.coin_w_right, 8, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.coin_u[self.frame_Sprite],
                          94, constants.coin_w_left, 8, 0)

        else:

            if self.direct == "right":
                pyxel.blt(self.x, self.y, 0, constants.coin_u2[self.frame_Sprite],
                          94, constants.coin_w_right, 8, 0)

            elif self.direct == "left":
                pyxel.blt(self.x, self.y, 0, constants.coin_u2[self.frame_Sprite],
                          94, constants.coin_w_left, 8, 0)

    # Updates the sprite #
    def update(self):
        self.move()
        self.coin_list()
        for i in range(len(self.list_coins)):

            if pyxel.frame_count % 3 == 0:
                self.list_coins[i].frame_Sprite += 1

        if not self.is_alive:
            self.frame_Sprite = 0

        if self.direct != "left" and self.direct != "right":
            self.spawn = random.randint(0, 1)

            if self.spawn == 1:
                self.direct = "left"

            else:
                self.direct = "right"

    # Defines its movement #
    def move(self):
        col_coin = Collisions(self.x, self.y, self.level)
        col_coin.detect_collision_en()

        if self.direct == "right":
            self.x += 1.5

            if self.x >= 256 - 8:
                self.direct = "left"

        elif self.direct == "left":
            self.x -= 1.5

            if self.x <= - 8:
                self.direct = "right"

        if col_coin.col_down:
            self.fall = False
            self.y = col_coin.y_tile * 8 + 1

        else:
            self.fall = True

        if self.fall:
            self.jump_speed = 5
            self.y += self.jump_speed

            # Establish a max speed #
            if self.jump_speed < 7:
                self.jump_speed += 1

        if self.y == 233 and self.x <= 24:
            self.y = 0
            self.direct = "right"

        if self.y == 233 and self.x >= 218:
            self.y = 0
            self.direct = "left"

    # Creates a list with coin objects #
    def coin_list(self):

        if pyxel.frame_count % 230 == 0:
            Coin1 = Coin()
            self.list_coins.append(Coin1)


class Pow(Sprite):

    def __init__(self):
        super().__init__()
        self.x = 120
        self.y = 20

    def update(self):

        # If the block is hit thrice, it "dies" #
        if self.change == 3:
            self.is_alive = False

        else:
            self.is_alive = True

    # Draws the sprite of the Pow depending on how many hits it has taken #
    def draw(self):
        pyxel.blt(self.x, self.y, 0, constants.pow_u[self.change], 104, constants.pow_w, 16)
