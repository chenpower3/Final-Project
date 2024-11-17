import pyxel


class Collisions:

    def __init__(self, x: float, y: float, level: int):
        self.platform_tile1 = (8, 13)
        self.platform_tile2 = (9, 13)
        self.x = x
        self.y = y
        self.x_tile = x // 8
        self.y_tile = y // 8
        self.col_down = False
        self.col_up = False
        self.col_left = False
        self.col_right = False
        self.level = level

    # Detects platforms #
    def detect_collision_player(self):
        for i in range(2):

            # Checks if there is a collision or not with the platforms #
            for j in range(1, 3):

                if (pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile + 3) == self.platform_tile1
                        or pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile + 3) == self.platform_tile2):
                    self.col_down = True
                    return self.col_down

                elif (pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile) == self.platform_tile1
                        or pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile) == self.platform_tile2):
                    self.col_up = True
                    return self.col_up

                elif (pyxel.tilemap(self.level).pget(self.x_tile - 1, self.y_tile + j) == self.platform_tile1
                      or pyxel.tilemap(self.level).pget(self.x_tile - 1, self.y_tile + j) == self.platform_tile2):
                    self.col_left = True
                    return self.col_left

                elif (pyxel.tilemap(self.level).pget(self.x_tile + 1, self.y_tile + j) == self.platform_tile1
                      or pyxel.tilemap(self.level).pget(self.x_tile + 1, self.y_tile + j) == self.platform_tile2):
                    self.col_right = True
                    return self.col_right

            # If no collision is detected #
            self.col_right = False
            self.col_left = False
            self.col_up = False
            self.col_down = False

    # Different collision for enemies, they have a different height and width #
    def detect_collision_en(self):
        for i in range(2):

            if (pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile + 2) == self.platform_tile1
                    or pyxel.tilemap(self.level).pget(self.x_tile + i, self.y_tile + 2) == self.platform_tile2):
                self.col_down = True
                return self.col_down

            # If no collision is detected #
            self.col_right = False
            self.col_left = False
            self.col_down = False
