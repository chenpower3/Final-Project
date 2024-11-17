# This class contains all the constants if we were to change any#
class Constants:
    def __init__(self):
        # Values to change the sprite from the character and game #

        self.game_height = 256
        self.game_width = 256
        self.lives = 3

        # Characteristics of the program, better not to change, mostly the editor's coordinates #
        # and default player spawn #
        self.__u = (0, 18, 33)
        self.__player_h = 24
        self.__player_w_right = (15, 11, 13)
        self.__player_w_left = (-15, -11, -13)
        self.__y = self.game_height - self.__player_h - 16
        self.__x = 128
        self.__dx = 4
        self.__en_u = (0, 16, 32)
        self.__en_u2 = (96, 112, 128)
        self.__en_sleep = (48, 64)
        self.__en_sleep2 = (144, 160)
        self.__en_w_right = 15
        self.__en_w_left = -15
        self.__coin_u = (3, 19, 35, 51, 67)
        self.__coin_u2 = (83, 99, 115, 131, 147)
        self.__coin_w_right = 16
        self.__coin_w_left = -16
        self.__pow_u = (0, 16, 32)
        self.__pow_w = 16

    @property
    def pow_u(self):
        return self.__pow_u

    @property
    def pow_w(self):
        return self.__pow_w

    @property
    def coin_w_right(self):
        return self.__coin_w_right

    @property
    def coin_w_left(self):
        return self.__coin_w_left

    @property
    def coin_u(self):
        return self.__coin_u

    @property
    def coin_u2(self):
        return self.__coin_u2

    @property
    def en_sleep(self):
        return self.__en_sleep

    @property
    def en_u(self):
        return self.__en_u

    @property
    def en_sleep2(self):
        return self.__en_sleep2

    @property
    def en_u2(self):
        return self.__en_u2

    @property
    def en_w_right(self):
        return self.__en_w_right

    @property
    def en_w_left(self):
        return self.__en_w_left

    @property
    def y(self):
        return self.__y

    @property
    def x(self):
        return self.__x

    @property
    def player_h(self):
        return self.__player_h

    @property
    def player_w_right(self):
        return self.__player_w_right

    @property
    def player_w_left(self):
        return self.__player_w_left

    @property
    def u(self):
        return self.__u

    @property
    def dx(self):
        return self.__dx

    @dx.setter
    def dx(self, dx: int or float):

        if not isinstance(dx, float) and not isinstance(dx, int):
            raise TypeError("dx must be an int or a float")

        else:
            self.__dx = dx

    @property
    def game_height(self):
        return self.__game_height

    @game_height.setter
    def game_height(self, game_height):

        if not isinstance(game_height, int):
            raise TypeError("game_height must be an int")

        if 0 > game_height or game_height > 256:
            raise ValueError("The game_height must be between 0 and 256")

        else:
            self.__game_height = game_height

    @property
    def game_width(self):
        return self.__game_width

    @game_width.setter
    def game_width(self, game_width):

        if not isinstance(game_width, int):
            raise TypeError("game_width must be an int")

        if 0 > game_width or game_width > 256:
            raise ValueError("The game_width must be between 0 and 256")

        else:
            self.__game_width = game_width

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, lives):

        if not isinstance(lives, int):
            raise TypeError("game_width must be an int")

        if 0 > lives:
            raise ValueError("lives can't be below 0")

        else:
            self.__lives = lives