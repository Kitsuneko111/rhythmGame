try:
    import pygame
except ImportError:
    raise(Exception('You will need to download pygame for this!'))
import tkinter as tk

print(pygame.font.get_fonts())


class View:
    """class for controlling the overall frontend"""
    def __init__(self):
        pygame.init()
        self.c = None
        self.game = None
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu('main')
        self.main_menu.register(self)
        self.mixer = pygame.mixer
        self.win = pygame.display.set_mode((512, 512))
        self.songname = ''

    def ask_player_name(self):
        return input("Enter Player Name: ")

    def quit(self):
        pygame.quit()
        self.main_menu.run = False

    def register(self, controller):
        self.c = controller

    def get_buttons(self, menu):
        center = self.c.get_player_center()
        return self.c.get_buttons(menu, center[0], center[1])

    def get_statics(self, menu):
        return self.c.get_statics(menu)

    def pressed(self, button, menu):
        self.c.pressed(button, menu)

    def run_view(self):
        self.main_menu.initialise()

    def play_song(self, songname):
        """control the playing of the requested song"""
        self.mixer.init()
        self.mixer.music.load(songname)
        self.mixer.music.set_endevent(pygame.USEREVENT+1)
        self.mixer.music.play(0)

    def stop_song(self):
        self.mixer.quit()

    def setBPM(self, bpm):
        self.c.set_bpm(bpm)

    def run_game(self, songname):

        self.songname = songname
        self.c.stop()
        self.game = Game(self.c, self)
        self.play_song(songname)
        self.c.set_jump_min()
        run = True
        while run:
            self.clock.tick(30)
            self.game.tick += 1
            if self.c.get_lives() <= 0:
                # checks for out of lives
                self.mixer.music.stop()
                print(self.c.get_points())
                run = False

            for event in pygame.event.get():
                # checks for quit
                if event.type == pygame.QUIT:
                    run = False
                # checks for song end
                if event.type == pygame.USEREVENT+1:
                    print(self.c.get_points())
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                # print('space')
                self.c.jump()

            if keys[pygame.K_LEFT]:
                self.game.move_player(-1, 0)

            if keys[pygame.K_RIGHT]:
                self.game.move_player(1, 0)

            if keys[pygame.K_UP]:
                self.game.move_player(0, -1)

            if keys[pygame.K_DOWN]:
                self.game.move_player(0, 1)

            self.game.redraw_game_window()
        # pygame.quit()
        self.stop_song()
        self.c.end()
        self.main_menu.initialise(self.c.get_points())


class Menu:
    """class for frontend menu control"""
    def __init__(self, name):
        self.name = name
        self._view = None
        self.trails = []
        self.font_type = 'bauhaus93'
        self.pressed = False

    def register(self, view):
        self._view = view

    def draw_player(self):
        # draws the player
        center = self._view.c.get_player_center()
        size = self._view.c.get_player_size()
        pygame.draw.rect(self._view.win, (255, 255, 255),
                         (center[0]-size[0]//2, center[1]-size[1]//2, size[0], size[1]))

    def draw_menu(self):
        # draws the menu
        pygame.draw.rect(self._view.win, (0, 0, 0), (0, 0, 512, 512))
        self.draw_buttons()
        self.draw_statics()
        self.add_trail()
        self.draw_trails()
        self.draw_player()
        pygame.display.update()

    def draw_statics(self):
        statics = self._view.get_statics('Main')
        #print(statics)
        for static in statics:
            x = static[1]
            y = static[2]
            width = static[4]
            height = static[3]
            colour = static[5] if not static[7] else static[6]
            pygame.draw.rect(self._view.win, colour, (x - width // 2, y - height // 2, width, height), width=0,
                             border_radius=22)
            font = pygame.font.Font('Play-Bold.ttf', static[8])
            render = font.render(static[0], True, (250, 88, 70))
            size = render.get_size()
            self._view.win.blit(render, (x - size[0] // 2, y - size[1] // 2 - 5))

    def draw_buttons(self):
        # draws the buttons
        buttons = self._view.get_buttons('Main')
        for button in buttons:
            x = button[1]
            y = button[2]
            width = button[4]
            height = button[3]
            colour = button[5] if not button[7] else button[6]
            pygame.draw.rect(self._view.win, colour, (x-width//2, y-height//2, width, height), width=0, border_radius=22)
            text = button[0].split("\n")
            ofont = pygame.font.Font("Play-Bold.ttf", button[8])
            orender = ofont.render(button[0], True, (0,0,0))
            osize = list(orender.get_size())
            osize[1] *= len(text)
            for i in range(len(text)):
                font = pygame.font.Font('Play-Bold.ttf', button[8])
                render = font.render(text[i], True, (250, 88, 70))
                size = render.get_size()
                self._view.win.blit(render, (x-size[0]//2, y-size[1]*(1-(i+1))//len(text)-15-(osize[1]*0.2)-10*len(text)+10*(i+1)))

    def add_trail(self):
        self.trails.append([self._view.c.get_player_center(), 10, 3])

    def rem_trail(self):
        self.trails.pop(0)

    def draw_trails(self):
        """handles the trail"""
        for trail in self.trails:
            pygame.draw.polygon(self._view.win, (255, 36, 160, 175),
                                ((trail[0][0], trail[0][1]-trail[1]//2),
                                 (trail[0][0]+trail[1]//2, trail[0][1]),
                                 (trail[0][0], trail[0][1]+trail[1]//2),
                                 (trail[0][0] - trail[1]//2, trail[0][1])))
            trail[1] = trail[1]-1
            if trail[1] < 0:
                self.rem_trail()


class MainMenu(Menu):
    """subclass for the main menu"""
    def __init__(self, name):
        super().__init__(name)
        self.run = True

    def initialise(self, points=None):
        """runs the menu frontend"""
        pygame.display.set_caption('Rhythm Game - Main Menu')
        stop = False
        while self.run:
            self._view.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    stop = True
                    pygame.quit()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                buttons = self._view.get_buttons('Main')
                for button in buttons:
                    if button[7] and not self.pressed:
                        self.pressed = True
                        self._view.pressed(button[0], 'Main')

            else:
                self.pressed = False

            if keys[pygame.K_LEFT]:
                self._view.c.move_player(-1, 0)

            if keys[pygame.K_RIGHT]:
                self._view.c.move_player(1, 0)

            if keys[pygame.K_UP]:
                self._view.c.move_player(0, -1)

            if keys[pygame.K_DOWN]:
                self._view.c.move_player(0, 1)

            if self.run:
                self.draw_menu()


class Game:
    """class for game control"""
    def __init__(self, c, view):
        self.trails = []
        self.c = c
        pygame.display.set_caption("Rhythm Game")
        self.tick = 0
        self.view = view

    def draw_player(self):
        """draws the player"""
        center = self.c.get_player_center()
        size = self.c.get_player_size()
        jump_off = self.c.get_jump()
        percent = (jump_off[1]-jump_off[0])/jump_off[1]
        if percent > 0.999:
            percent = 0
        colour = 255 * percent
        pygame.draw.rect(self.view.win, (255, 255-(colour//2), 255-colour),
                         (center[0]-size[0]//2, center[1]-size[1]//2, size[0], size[1]))

    def redraw_game_window(self):
        """draws the window"""
        pygame.draw.rect(self.view.win, (0, 0, 0), (0, 0, 512, 512))
        self.draw_trails()
        self.add_trail()
        self.draw_obstacles()
        self.draw_player()
        pygame.display.update()
        pygame.display.set_caption(('Rhythm Game - '+self.view.songname.split('/')[-1]+' | '+str(self.c.get_lives())+' lives; ' +
                                    str(self.c.get_points())+' points'))

    def move_player(self, x, y):
        self.c.move_player(x, y)

    def add_trail(self):
        self.trails.append([self.c.get_player_center(), 10, 3])

    def rem_trail(self):
        self.trails.pop(0)

    def draw_trails(self):
        """draws the trail"""
        for trail in self.trails:
            pygame.draw.polygon(self.view.win, (255, 36, 160, 175),
                                ((trail[0][0], trail[0][1]-trail[1]//2),
                                 (trail[0][0]+trail[1]//2, trail[0][1]),
                                 (trail[0][0], trail[0][1]+trail[1]//2),
                                 (trail[0][0] - trail[1]//2, trail[0][1])))
            trail[1] = trail[1]-1
            if trail[1] < 0:
                self.rem_trail()

    def draw_obstacles(self):
        """draws the obstacles"""
        obstacles = self.c.get_obstacles()
        for obstacle in obstacles:
            if obstacle.dummy:
                continue
            if obstacle.start > self.tick:
                continue
            if not obstacle.active:
                pygame.draw.polygon(self.view.win, (250, 88, 70), obstacle.points)
            else:
                pygame.draw.polygon(self.view.win, (132, 242, 250), obstacle.points)
