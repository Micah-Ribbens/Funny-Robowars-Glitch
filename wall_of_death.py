import pygame
from important_variables import (
    win,
    screen_height,
    screen_width, 
    consistency_keeper
)
class WallOfDeath:
    color = (0, 0, 250)
    x_coordinate = 0
    y_coordinate = 0
    height = screen_height
    length = 0
    movement = screen_width * 0.0002
    def _improve_variables():
        WallOfDeath.movement = consistency_keeper.calculate_new_speed(WallOfDeath.movement)
    def draw():
        pygame.draw.rect(win, (WallOfDeath.color), (WallOfDeath.x_coordinate,
                                WallOfDeath.y_coordinate, WallOfDeath.length, WallOfDeath.height))

    def move():
        if WallOfDeath.x_coordinate + WallOfDeath.movement <= 0:
            WallOfDeath.x_coordinate += WallOfDeath.movement
        else:
            excess = WallOfDeath.movement + WallOfDeath.x_coordinate
            WallOfDeath.x_coordinate = 0
            WallOfDeath.length += excess
    def move_backwards(amount):
        if WallOfDeath.length >= amount:
            WallOfDeath.length -= amount
        else:
            excess = amount - WallOfDeath.length
            WallOfDeath.length = WallOfDeath.length - amount + excess
            WallOfDeath.x_coordinate -= excess
    def reset():
        WallOfDeath.length = 10
        WallOfDeath.x_coordinate = 0
    def move_backwards(amount):
        if WallOfDeath.length >= amount:
            WallOfDeath.length -= amount
        else:
            excess = amount - WallOfDeath.length
            WallOfDeath.length = WallOfDeath.length - amount + excess
            WallOfDeath.x_coordinate -= excess
    def reset():
        WallOfDeath.length = 10
        WallOfDeath.x_coordinate = -100