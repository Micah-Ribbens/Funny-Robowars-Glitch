from important_variables import (
    screen_height,
    screen_width,
    win,
    consistency_keeper
)
import pygame
from time import time
import math

class Player:
    is_facing_right = True
    full_health = 20
    current_health = full_health
    player_color = (250, 0, 0)
    x_coordinate = 100
    y_coordinate = screen_height - 200
    width = screen_width * .05
    height = screen_height * .15
    movement = screen_width * 0.0004
    movement_down = screen_height * .002
    jumped = 0
    can_move_down = True
    on_platform = False
    can_move_left = True
    can_move_right = True
    move_right = False
    can_jump = True
    is_jumping = False
    jump_height = screen_height * .002
    max_jump_height = screen_height * .4
    jump_key_held_down = False
    throw_whip = False
    space_held_in = False
    # So player hangs a bit in air when reaches max jump height
    stay_up_in_air = False
    stationary_air_time = 0

    def _improve_variables(self):
        self.movement = screen_width * (
            consistency_keeper.calculate_new_speed(0.0004))

        self.movement_down = screen_height * (
            consistency_keeper.calculate_new_speed(.002))

        self.jump_height = screen_height * (
            consistency_keeper.calculate_new_speed(.002))

    def draw(self):
        pygame.draw.rect(win, (self.player_color), (self.x_coordinate,
                         self.y_coordinate, self.width, self.height))

    def is_dead(self):
        if self.current_health == 0:
            return True

        return False

    def movements(self):
        controlls = pygame.key.get_pressed()
        self._improve_variables()
        if self.jump_key_held_down and self.on_platform:
            self.can_jump = False

        elif self.on_platform:
            self.can_jump = True

        move_right_possible = controlls[pygame.K_RIGHT] and self.can_move_right

        if move_right_possible:
            self.is_facing_right = True

        if move_right_possible and self.x_coordinate >= screen_width * .2:
            self.move_right = True

        elif move_right_possible:
            self.x_coordinate += self.movement

        else:
            self.move_right = False

        if controlls[pygame.K_LEFT] and self.can_move_left:
            self.x_coordinate -= self.movement
            self.is_facing_right = False

        if controlls[pygame.K_UP]:
            self.jump_key_held_down = True

        else: 
            self.jump_key_held_down = False

        if self.is_jumping and not self.can_jump:
            self.stay_up_in_air = True
        
        elif self.can_jump and self.jump_key_held_down:
            self.jump()
        
        if self.stay_up_in_air or (self.is_jumping and not self.jump_key_held_down):
            # print("DO A APEX")
            self.apex()

        if controlls[pygame.K_DOWN] and self.can_move_down:
            self.y_coordinate += self.movement_down

        if controlls[pygame.K_SPACE] and not self.space_held_in:
            self.throw_whip = True
            self.space_held_in = True

        else:
            self.throw_whip = False

        if not controlls[pygame.K_SPACE]:
            self.space_held_in = False

    def apex(self):
        stationary_time_needed = .1
        if self.stationary_air_time >= stationary_time_needed:
            self.is_jumping = False
            self.stay_up_in_air = False
            self.stationary_air_time = 0

        else:
            self.stationary_air_time += consistency_keeper.current_speed

    def jump(self):
        if self.on_platform:
            self.jumped = 0 + self.jump_height
            self.is_jumping = True

        if self.jumped <= self.max_jump_height and self.is_jumping:
            self.y_coordinate -= self.jump_height
            self.jumped += self.jump_height

        if self.jumped >= self.max_jump_height:
            self.can_jump = False

    def controls(self):
        self.movements()
    
    def max_jump_time(self, new_platform_y_coordinate, last_platform_y_coordinate, gravity):
        # print(last_platform.y_coordinate)
        # print(new_platform_y_coordinate, last_platform_y_coordinate)
        # print("LAST Y COR ", last_platform_y_coordinate)
        # print("NEW Y COR: ", new_platform_y_coordinate)
        # print("MAX JUMP: ", self.max_jump_height)
        # print("JUMP PER THING: ", self.jump_height)
        # print("GRAVITY: ", gravity)
        upwards_time = 0
        max_y_coordinate = 0
        # Top of screen is 0, but for simpler calculations I'll treat it as 500
        if last_platform_y_coordinate - self.max_jump_height <= 0:
            upwards_time = math.ceil((last_platform_y_coordinate - self.height) / self.jump_height)
            max_y_coordinate = self.height

        else:
            # print("I WAS CALLED")
            max_y_coordinate = last_platform_y_coordinate - self.max_jump_height
            upwards_time = math.ceil(self.max_jump_height / self.jump_height)
        
        # print("UPWARDS: ", upwards_time)
        downwards_time = math.ceil((new_platform_y_coordinate - max_y_coordinate) / gravity)
        # print("max y coordinate: ", max_y_coordinate)
        # print("dt: ", downwards_time, " ut: ", upwards_time)
        return upwards_time + downwards_time

    def reset_player_location(self):
        self.x_coordinate = 50
        self.y_coordinate = 50

    def knockback_left(self):
        self.x_coordinate -= 75
        self.current_health -= 10

    def knockback_right(self):
        self.x_coordinate += 75
        self.current_health -= 10

