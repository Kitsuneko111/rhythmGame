import pygame
from playsound import playsound
from appJar import gui


class View:
    def __init__(self):
        self._c = None
        self.game = None
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu('main')
        self.main_menu.register(self)

    def register(self, controller):
        self._c = controller
        ##self.game = Game(controller)

    def run_view(self):
        self.main_menu.initialise()

    def play_song(self, songname):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.load(songname)
        self.mixer.music.set_endevent(pygame.USEREVENT+1)
        self.mixer.music.play(0)

    def stop_song(self):
        self.mixer.quit()

    def run_game(self, songname):
        self._c.stop()
        self.game = Game(self._c)
        self.main_menu.app.removeAllWidgets()
        self.main_menu.app.stop()
        ##songname = input('Song\n>>> ')
        self.play_song(songname)
        run = True
        while run:
            self.clock.tick(27)

            if self._c.get_lives() <= 0:
                self.mixer.music.stop()
                print(self._c.get_points())
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.USEREVENT+1:
                    print(self._c.get_points())
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ##print('moving left')
                self.game.move_player(-1, 0)

            if keys[pygame.K_RIGHT]:
                ##print('moving right')
                self.game.move_player(1, 0)

            if keys[pygame.K_UP]:
                ##print('moving up')
                self.game.move_player(0, -1)

            if keys[pygame.K_DOWN]:
                ##print('moving down')
                self.game.move_player(0, 1)
            self.game.redraw_game_window()
        pygame.quit()
        self.main_menu.initialise(self._c.get_points())

class Menu():
    def __init__(self, name):
        self.name = name
        self._view = None

    def register(self, view):
        self._view = view

    def run_game(self, songname):
        self._view.run_game(songname)


class MainMenu(Menu):
    def __init__(self, name):
        super().__init__(name)
        self.app = None
    def initialise(self, points = None):
        self.app = gui(size='512x512', title='Rhythm Game - Menu')
        print(points)
        if points:
            points = 'Points: '+str(points)
            ##print(points)
            self.app.addLabel('score', points)
        self.app.addButton('start', self.run_game, row=2)
        self.app.addEntry('songname', row=1)
        self.app.go()

    def run_game(self):
        if self.app.getEntry('songname'):
            super().run_game(self.app.getEntry('songname'))


class Game:
    def __init__(self, c):
        self.trails = []
        self._c = c
        pygame.init()
        self.win = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("Rhythm Game")

    def draw_player(self):
        center = self._c.get_player_center()
        size = self._c.get_player_size()
        pygame.draw.rect(self.win, (255, 255, 255), (center[0]-size[0]//2, center[1]-size[1]//2, size[0], size[1]))

    def redraw_game_window(self):
        pygame.draw.rect(self.win, (0, 0, 0), (0, 0, 512, 512))
        self.draw_trails()
        self.add_trail()
        self.draw_obstacles()
        self.draw_player()
        pygame.display.update()
        pygame.display.set_caption(('Rhythm Game - '+str(self._c.get_lives())+' lives; '+str(self._c.get_points())+' points'))

    def move_player(self, x, y):
        self._c.move_player(x, y)

    def add_trail(self):
        self.trails.append([self._c.get_player_center(), 10, 3])

    def rem_trail(self):
        self.trails.pop(0)

    def draw_trails(self):
        for trail in self.trails:
            pygame.draw.polygon(self.win, (255, 36, 160, 175), ((trail[0][0], trail[0][1]-trail[1]//2), (trail[0][0]+trail[1]//2, trail[0][1]), (trail[0][0], trail[0][1]+trail[1]//2), (trail[0][0]-trail[1]//2, trail[0][1])))
            trail[1] = trail[1]-1
            if trail[1] < 0:
                self.rem_trail()

    def draw_obstacles(self):
        obstacles = self._c.get_obstacles()
        for obstacle in obstacles:
            if not obstacle.active:
                pygame.draw.rect(self.win, (250, 88, 70), (obstacle.x-obstacle.width//2, obstacle.y, obstacle.width, 512))
            else:
                pygame.draw.rect(self.win, (132, 242, 250), (obstacle.x-obstacle.width//2, obstacle.y, obstacle.width, 512))
