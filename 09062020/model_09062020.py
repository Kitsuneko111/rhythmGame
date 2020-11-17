from random import randint
import pygame

class Menu:
    def __init__(self, name):
        self.name = name


class MainMenu(Menu):
    def __init__(self):
        super().__init__('Main')


class Player:
    def __init__(self, pos_x = 256, pos_y = 256, vel = 9, lives = 5, points = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.lives = lives
        self.vel = vel
        self.width = 16
        self.height = 16
        self.points = points

    def move(self, x_move, y_move):
        if 0+self.width//2 < x_move+self.pos_x < 512-self.width//2:
            ##print('moving')
            self.pos_x += int(x_move)
        if 0+self.height//2 < y_move+self.pos_y < 512-self.height//2:
            self.pos_y += y_move


class Obstacle:
    def __init__(self, x=256, y=0, rot=0, width=32, life = 5, active = 20):
        self.x = x
        self.y = y
        self.rot = rot
        self.width = width
        self.life = life
        self.active = active
        self.hit = False


class Model:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.clock = pygame.time.Clock()

    def add_obstacle(self, x=256, y=0, rot=0, width=32):
        self.obstacles.append(Obstacle(x, y, rot, width))

    def rem_obstacle(self, pos=0):
        ##print('removed')
        self.obstacles.pop(pos)
        self.player.points += 1

    def check_rem(self):
        ##print('checking')
        for i in range(len(self.obstacles)-1):
            ##print(self.obstacles[i].life)
            if self.obstacles[i].life <= 0:
                ##print('yes')
                self.rem_obstacle(i)

    def calculate_collision(self):
        player = self.player
        obstacles = self.obstacles
        player_left = player.pos_x-player.width//2
        player_right = player.pos_x+player.width//2
        player_top = player.pos_y-player.height//2
        player_bottom = player.pos_y+player.height//2
        for obstacle in obstacles:
            obstacle_left = obstacle.x-obstacle.width//2
            obstacle_right = obstacle.x+obstacle.width//2
            if not obstacle.active and not obstacle.hit and player_left < obstacle_right and player_right > obstacle_left:
                player.lives -= 1
                obstacle.hit = True

    def trigger_obstacle_creation(self):
        ##print(len(self.obstacles))
        self.calculate_collision()
        for obstacle in self.obstacles:
            if not obstacle.active:
                obstacle.life -= 1
            else:
                obstacle.active -=1
        self.check_rem()
        creation_chance = randint(1, 20)
        ##print('triggered')
        if creation_chance == 1:
            ##print('creating')
            width = randint(10, 128)
            x = randint(0+width//2, 512-width//2)
            self.add_obstacle(x=x, width=width)
