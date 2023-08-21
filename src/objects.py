import pygame as pg
from random import randrange

# Vector2
v2 = pg.math.Vector2


class Snake:
    # Snake object constructor
    def __init__(self, game):
        self._game = game
        self._size = game.tile_size
        self._range = self._size//2, self._game.window_size - self._size//2, self._size
        self._rect = pg.rect.Rect([0, 0 , self._size - 2, self._size - 2])
        self._rect.center = self._random_position()
        self._direction = v2(0, 0)
        self.__step_delay = 100
        self.__time = 0
        self.__length = 1
        self.__segments = []
        self.__direction_crtl = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
        

    # Rectangle getter
    @property
    def rect(self):
        return self._rect
    
    # Public control method to control the snake and control that player cannot move the snake to opposite direction
    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.__direction_crtl[pg.K_UP]:
                self._direction = v2(0, -self._size)
                self.__direction_crtl = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_DOWN and self.__direction_crtl[pg.K_DOWN]:
                self._direction = v2(0, self._size)
                self.__direction_crtl = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_LEFT and self.__direction_crtl[pg.K_LEFT]:
                self._direction = v2(-self._size, 0)
                self.__direction_crtl = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if event.key == pg.K_RIGHT and self.__direction_crtl[pg.K_RIGHT]:
                self._direction = v2(self._size, 0)
                self.__direction_crtl = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
   
    # Private delta_time method to decrease the speed of the snake
    def __delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.__time > self.__step_delay:
            self.__time = time_now
            return True
        return False
    
    # Random position method
    def _random_position(self):
        return [randrange(*self._range), randrange(*self._range)]
    
    # Random position getter
    @property
    def random_position(self):
        return self._random_position()
    
    # Private check area method. When the snake goes out of the area -> new game
    def __check_area(self):
        if self._rect.left < 0 or self._rect.right > self._game.window_size:
            self._game.new_game()
        if self._rect.top < 0 or self._rect.bottom > self._game.window_size:
            self._game.new_game()

    # Private check food method. Checks when snake eats the food and increase the length of the snake and points
    def __check_food(self):
        if self._rect.center == self._game.food.rect.center:
            self._game.food.rect.center = self._random_position()
            self.__length += 1
            self._game.points()

    # Private check self collision method
    def __check_selfcollide(self):
        if len(self.__segments) != len(set(segment.center for segment in self.__segments)):
            self._game.new_game()

    # Private move method
    def __move(self):
        if self.__delta_time():
            self._rect.move_ip(self._direction)
            self.__segments.append(self._rect.copy())
            self.__segments = self.__segments[-self.__length:]

    # Public update method
    def update(self):
        self.__check_selfcollide()
        self.__check_area()
        self.__check_food()
        self.__move()

    # Public draw method
    def draw(self):
        [pg.draw.rect(self._game.screen, 'yellow', segment) for segment in self.__segments]
    
# Food class inherited from Snake object
class Food(Snake):
    def __init__(self, game):
        super().__init__(game)
       
    # Public draw method
    def draw(self):
        pg.draw.rect(self._game.screen, 'red', self._rect)

