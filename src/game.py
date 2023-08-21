import pygame as pg
from objects import *

# Counter generator function that increase the games attribute until it hits the maximum amount
def counter(max: int):
        games = 0
        while games <= max:
            yield games
            games += 1

# Set counter function for maximum games 
count = counter(4)

# Game class
class Game:
    # Game object constructor
    def __init__(self):
        pg.init()
        self.__window_size = 600
        self.__tile_size = 30
        self.__points = 0
        self.games = 0
        self.__screen = pg.display.set_mode((self.__window_size, self.__window_size))
        self._clock = pg.time.Clock()
        self.new_game()
        self.__bg = pg.image.load("./src/assets/backgrounds/background.png")
        self.__font = pg.font.Font("freesansbold.ttf", 16)
        self.__point_txt = self.__font.render(f"Points: {self.__points} Games: {self.games}/5", True, (0, 255, 0), (0, 0, 128))
        self.__txtRect = self.__point_txt.get_rect()
        self.__txtRect.center = (self.__window_size//2, 20)

    # Screen-size getter
    @property
    def window_size(self):
        return self.__window_size
    
    # Tile-size getter
    @property
    def tile_size(self):
        return self.__tile_size
    
    # Screen getter
    @property
    def screen(self):
        return self.__screen
    
    # Points method that increase points attribute when called
    def points(self):
        self.__points += 10

    # Recursive horizontal line method for grid in the screen
    def __recursive_h_line(self, y_coord: int, window_size: int, tile_size: int):
        pg.draw.line(self.__screen, (255, 255, 255), (0, y_coord), (window_size , y_coord), 1)


        if (y_coord <= window_size):
            y_coord += tile_size
            self.__recursive_h_line(y_coord, window_size, tile_size)
    
    # Recursive vertical line method for grid in the screen
    def __recursive_v_line(self, x_coord: int, window_size: int, tile_size: int):
        pg.draw.line(self.__screen, (255, 255, 255), (x_coord, 0), (x_coord, window_size), 1)


        if (x_coord <= window_size):
            x_coord += tile_size
            self.__recursive_v_line(x_coord, window_size, tile_size)

    # Public new_game method that creates snake and food objects and increase the count generator
    def new_game(self):
        try:
            next(count)
            self.games += 1
            self.__snake = Snake(self)
            self.__food = Food(self)
    
        except StopIteration:
            exit()

    # Snake getter
    @property
    def snake(self):
        return self.__snake
    
    # Food getter
    @property
    def food(self):
        return self.__food
    
    # Private update-method that update snake-object, screen and points count and games left text bar  
    def __update(self):
        self.__point_txt = self.__font.render(f"Points: {self.__points} Games: {self.games}/5", True, (0, 255, 0), (0, 0, 128))
        self.__screen.blit(self.__point_txt, self.__txtRect)
        self.__snake.update()
        pg.display.flip()
        self._clock.tick(60)

    # Private draw-method that set window caption, fill the screen, show the background image, creates recursive grid lines and draw snake and food
    def __draw(self):
        pg.display.set_caption("Snake Game")
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.__bg, (0, 0))
        self.__recursive_h_line(0, self.__window_size, self.__tile_size)
        self.__recursive_v_line(0, self.__window_size, self.__tile_size)
        self.__snake.draw()
        self.__food.draw()
        

    # Private check_event-method that take events for game quit and snake control
    def __check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            self.__snake.control(event)

    # Public run-method that check events, update and draw methods
    def run(self):
        while True:
            self.__check_event()
            self.__update()
            self.__draw()