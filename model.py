from random import randint
import math
import sqlite3


class Menu:
    """Main class for all menus"""
    def __init__(self, name, buttons, statics):
        self.name = name
        self.buttons = buttons
        self._m: Model = None
        self.statics = statics

    def register(self, model):
        self._m = model

    def return_button_info(self, x, y, button=None):
        """returns the info needed about a button(s)"""
        if button:
            self.buttons[button].check_pressed(x, y)
            self.buttons[button].info[7] = self.buttons[button].pressed
            return self.buttons[button].info
        buttons = []
        for button in self.buttons:
            self.buttons[button].check_pressed(x, y)
            self.buttons[button].info[7] = self.buttons[button].pressed
            buttons.append(self.buttons[button].info)
        return buttons

    def return_statics_info(self, static=None):
        if static:
            return self.statics[static].get_info()
        else:
            statics = []
            for static in self.statics:
                statics.append(static.get_info())
            return statics


class Scoreboard(Menu):
    def __init__(self):
        super().__init__("Scores", {
            "Back": Button("Back", 50, 25, 40, 75, (6, 37, 191), (82, 215, 255), 25, lambda: self._m.stop_scores())
        },
                         [
                             Button("Scoreboard", 256, 65, 45, 350, (6, 37, 191), (82, 215, 255), 35, lambda: None),
                             Button("1", 256, 125, 35, 325, (6, 37, 191), (82, 215, 255), 35, lambda: None),
                             Button("2", 256, 165, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda:None),
                             Button("3", 256, 205, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("4", 256, 245, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("5", 256, 285, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("6", 256, 325, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("7", 256, 365, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("8", 256, 405, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("9", 256, 445, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),
                             Button("10", 256, 485, 35, 325, (6, 3, 191), (82, 215, 255), 35, lambda: None),

                         ])

    def top_10(self):
        for i in range(10):
            self.statics[i+1].name = str(i+1)
        results = self._m.return_scores()
        for i in range(len(results)):
            player = self._m.get_player(results[i][1])
            self.statics[i+1].name = player+" - "+str(results[i][0])


class MainMenu(Menu):
    """specific requirements for the main menu"""
    def __init__(self):
        super().__init__('Main', {
            "Start": Button('Start', 256, 282, 115, 240, (6, 37, 191), (82, 215, 255), 90,
                            lambda: self._m.run_game()),
            "Random\nSong": Button("Random\nSong", 128, 150, 110, 230, (6, 37, 191), (82, 215, 255), 40,
                                  lambda: self.randomise_song()),
            "Change\nDifficulty": Button("Change\nDifficulty", 256+128, 150, 110, 230, (6, 37, 191), (82, 215, 255), 40,
                                         lambda: self.change_difficulty()),
            "Quit": Button("Quit", 256, 450, 50, 100, (6, 37, 191), (82, 215, 255), 30, lambda: self._m.quit()),
            "Scores": Button("Scores", 256, 382, 57, 125, (6, 37, 191), (82, 215, 255), 35, lambda: self._m.show_scores())
        },
                         [
                             Button("None", 256, 50, 50, 475, (6, 37, 191), (82, 215, 255), 25,
                                    lambda: None)
                         ])

    def randomise_song(self):
        self._m.track_no = randint(0, len(self._m.songs)-1)
        self.statics[0].name = self._m.songs[self._m.track_no][0].split('/')[-1]+' - '+self._m.diffNames[self._m.difficulty]
        print(self._m.songs[self._m.track_no])

    def change_difficulty(self):
        self._m.difficulty = (self._m.difficulty + 1) % len(self._m.difficulties)
        self.statics[0].name = self._m.songs[self._m.track_no][0].split('/')[-1]+' - '+self._m.diffNames[self._m.difficulty]
        print(self._m.difficulty)


class Button:
    """class for a button for organisation"""
    def __init__(self, name, x, y, height, width, colour, colour_pressed, text, action=lambda: print('no function')):
        self.name = name
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.colour_pressed = colour_pressed
        self.pressed = False
        self.text = text
        self.info = [name, x, y, height, width, colour, colour_pressed, False, text]
        self.press = action

    def get_info(self):
        self.info[0] = self.name
        return self.info

    def check_pressed(self, x, y):
        if self.x-self.width//2 < x < self.x+self.width//2 and self.y-self.height//2 < y < self.y+self.height//2:
            self.pressed = True
        else:
            self.pressed = False


class Player:
    """class for a player"""
    def __init__(self, pos_x=256, pos_y=256, vel=6, lives=5, points=0, jumpvel=5, max_jump=0.4, jump_min=4000):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.lives = lives
        self.vel = vel
        self.width = 16
        self.height = 16
        self.points = points
        self.jumpvel = jumpvel
        self.jump = 0
        self.max_jump = max_jump
        self.jump_off = 0
        self.jump_min = jump_min

    def move(self, x_move, y_move):
        if 0+self.width//2 < x_move+self.pos_x < 512-self.width//2:
            self.pos_x += int(x_move)
        if 0+self.height//2 < y_move+self.pos_y < 512-self.height//2:
            self.pos_y += y_move


class Obstacle:
    """class for the obstacles the players have to dodge"""
    def __init__(self, x=256, y=256, rot: float = 0, width=32, life=5, active=20, start=0, dummy=False):
        self.x = x
        self.y = y
        self.rot = rot
        self.width = width
        self.life = life
        self.active = active
        self.hit = False
        self.dummy = dummy
        self.start = start
        self.points = None
        self.up = False
        self.right = False
        self.get_y1 = None
        self.get_y2 = None
        self.get_x1 = None
        self.get_x2 = None
        self.down = False

    def calculate_points(self):
        """very long mathmatical script to work out where the 'corners' of the obstacles are"""
        rot = 90-self.rot % 180
        if self.rot % 180 == 0:
            # checking if the rotation is 0 as this is hard to calculate otherwise
            self.up = True
            return self.calculate_points_0()
        # mathmatical notes to help visualise
        # y = mx + c
        # y' = (-1/m)x' + c'
        # a^2 + b^2 = c^2
        c = self.width/2
        # m is the change in y per 1 change in x
        rot = math.radians(rot)
        m = 0-math.tan(rot)
        if m == 0:
            # checking if the rotation is sideways as we can skip a lot of code if this is the case
            self.right = True
            return self.calculate_points_0(True)
        m1 = -1/m
        # delta*c^2 = delta*x^2 + delta*y^2
        rot1 = math.atan(m1)
        if m == abs(m):
            self.down = True
        x1 = c*math.cos(rot1)
        y1 = c*math.sin(rot1)
        # y-y1 = m(x-x1)
        c1 = m*(+x1)-y1+self.y
        c2 = m*(-x1)+y1+self.y
        self.get_y1 = lambda x: int(m*(x-self.x)+c1)
        self.get_y2 = lambda x: int(m*(x-self.x)+c2)
        self.get_x1 = lambda y: int(((y-c1)//m)+self.x)
        self.get_x2 = lambda y: int(((y-c2)//m)+self.x)
        # l1 = y=mx+c1
        # l2 = y=mx+c2
        # x = (y-c)/m
        # calculating all the points
        p11 = (0, int(m*(0-self.x)+c1))
        p12 = (int(((0-c1)//m)+self.x), 0)
        p13 = (512, int(m*(512-self.x)+c1))
        p14 = (int(((512-c1)//m)+self.x), 512)
        p21 = (0, int(m*(0-self.x)+c2))
        p22 = (int(((0 - c2)//m)+self.x), 0)
        p23 = (512, int(m*(512-self.x)+c2))
        p24 = (int(((512 - c2)//m)+self.x), 512)
        points = [p11, p12, p13, p14, p21, p22, p23, p24]

        points_rem = []
        # remove OOB points
        for i in range(8):
            if points[i][0] < 0 or points[i][0] > 512 or 512 < points[i][1] or points[i][1] < 0:
                points_rem.append(i)

        for i in range(len(points_rem)):
            points.pop(points_rem[i]-i)

        if len(points) == 4:
            # checking to see if the corners need placing
            points1 = [points[0], points[1]]
            points2 = [points[2], points[3]]
            left1 = False
            top1 = False
            right1 = False
            bottom1 = False
            left2 = False
            right2 = False
            top2 = False
            bottom2 = False
            if points1[0][0] == 0:
                left1 = True
            elif points1[0][0] == 512:
                right1 = True
            if points1[0][1] == 0:
                top1 = True
            elif points1[0][1] == 512:
                bottom1 = True
            if points1[1][0] == 0:
                left1 = True
            elif points1[1][0] == 512:
                right1 = True
            if points1[1][1] == 0:
                top1 = True
            elif points1[1][1] == 512:
                bottom1 = True

            if points2[0][0] == 0:
                left2 = True
            elif points2[0][0] == 512:
                right2 = True
            if points2[0][1] == 0:
                top2 = True
            elif points2[0][1] == 512:
                bottom2 = True
            if points2[1][0] == 0:
                left2 = True
            elif points2[1][0] == 512:
                right2 = True
            if points2[1][1] == 0:
                top2 = True
            elif points2[1][1] == 512:
                bottom2 = True

            tl = False
            tr = False
            bl = False
            br = False

            if top1 and right2:
                tr = True
            if left1 and top2:
                tl = True
            if bottom1 and left2:
                bl = True
            if right1 and bottom2:
                br = True
            if top1 and left2:
                tl = True
            if left1 and bottom2:
                bl = True
            if bottom1 and right2:
                br = True
            if right1 and top2:
                tr = True
            if tr:
                points.append((512, 0))
            if tl:
                points.append((0, 0))
            if bl:
                points.append((0, 512))
            if br:
                points.append((512, 512))

        else:
            top = False
            bottom = False
            left = False
            right = False
            if points[0][0] == 0:
                left = True
            elif points[0][0] == 512:
                right = True
            if points[0][1] == 0:
                top = True
            elif points[0][1] == 512:
                bottom = True
            if points[1][0] == 0:
                left = True
            elif points[1][0] == 512:
                right = True
            if points[1][1] == 0:
                top = True
            elif points[1][1] == 512:
                bottom = True

            if top and left:
                points.append((0, 0))
            elif top and right:
                points.append((512, 0))
            elif bottom and left:
                points.append((0, 512))
            elif bottom and right:
                points.append((512, 512))

        self.points = tuple(self.sort_points(points))

    def calculate_points_0(self, flip=False):
        """for calculating the easy points"""
        # print('0', flip)
        if not flip:
            self.up = True
            # print('up')
        if flip:
            self.right = True
        if flip:
            points = [(0, self.y-self.width//2 if self.y-self.width//2 >= 0 else 0),
                      (0, self.y+self.width//2 if self.y+self.width//2 <= 512 else 512),
                      (512, self.y-self.width//2 if self.y-self.width//2 >= 0 else 0),
                      (512, self.y+self.width//2 if self.y+self.width//2 <= 512 else 512)]
        else:
            points = [(self.x - self.width//2 if self.x - self.width // 2 >= 0 else 0, 0),
                      (self.x + self.width // 2 if self.x + self.width // 2 <= 512 else 512, 0),
                      (self.x - self.width // 2 if self.x - self.width // 2 >= 0 else 0, 512),
                      (self.x + self.width // 2 if self.x + self.width // 2 <= 512 else 512, 512)]
        self.points = tuple(self.sort_points(points))

    @staticmethod
    def clockwiseangle_and_distance(point, origin=(256, 256), refvec=(0, 1)):
        """copied from
        https://stackoverflow.com/questions/41855695/sorting-list-of-two-dimensional-coordinates-by-clockwise-angle-using-python
        on 02/07/2020 posted by MSeifert
        designed to sort the points into a clockwise order to allow correct displaying"""

        # Vector between point and the origin: v = p - o
        vector = [point[0] - origin[0], point[1] - origin[1]]
        # Length of vector: ||v||
        lenvector = math.hypot(vector[0], vector[1])
        # If length is zero there is no angle
        if lenvector == 0:
            return -math.pi, 0
        # Normalize vector: v/||v||
        normalized = [vector[0] / lenvector, vector[1] / lenvector]
        dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]  # x1*x2 + y1*y2
        diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]  # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        # Negative angles represent counter-clockwise angles so we need to subtract them
        # from 2*pi (360 degrees)
        if angle < 0:
            return 2 * math.pi + angle, lenvector
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle, lenvector

    def sort_points(self, points):
        return sorted(points, key=self.clockwiseangle_and_distance)


class Model:
    """overall class controlling all other classes"""
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.tick = 0
        self.bpm = -1
        self.tick_gap = -1
        self.difficulty = 0
        self.difficulties = [1, 2, 4, 30, 180]
        self.diffNames = ['Easiest', 'Easy', 'Normal', 'Hard', 'MAX']
        self.menus = {'Main': MainMenu(), "Scores": Scoreboard()}
        self.songs = [("./Astley.mp3", 113),
                      ("./The Piano Guys/So Far, So Good/03 - Fight Song _ Amazing Grace.mp3", 88),
                      ("./The Piano Guys/So Far, So Good/09 - Titanium _ Pavane.mp3", 127),
                      ("./The Fear.mp3", 134),
                      ("./Test2.ogg", 175),
                      ("./Ghost (3).ogg", 110)
                      ]
        self.track_no = 0
        self.register()
        self._c = None
        self.conn = sqlite3.connect("localData/database.db")
        self.db = self.conn.cursor()
        self.init_players()
        self.init_scores()

    def stop_scores(self):
        self._c.stop_scoreboard()

    def show_scores(self):
        self.menus["Scores"].top_10()
        self._c.scoreboard()

    def get_player(self, player_id):
        self.db.execute("select player_name from players where player_id = ?", [player_id])
        player = self.db.fetchone()
        print(player)
        return player[0]

    def return_scores(self, top=True):
        self.db.execute("select * from scores")
        scores = self.db.fetchall()
        print(scores)
        self.db.execute("select points, player_id from scores where song_name = ? and difficulty = ? order by points desc limit 10", [self.songs[self.track_no][0], self.difficulty])
        scores = self.db.fetchall()
        print(scores)
        return scores

    def init_scores(self):
        self.db.execute("create table if not exists scores(points integer, difficulty integer, song_name varchar("
                        "255), player_id integer, score_id integer "
                        "auto increment primary key, foreign key (player_id) references players(player_id))")

    def init_players(self):
        self.db.execute("create table if not exists players(player_name varchar(255), player_id integer "
                        "primary key autoincrement)")

    def quit(self):
        self._c.quit()

    def register_c(self, c):
        self._c = c

    def run_game(self):
        self.set_bpm(self.songs[self.track_no][1])
        if self.menus['Main'].statics[0].name != 'None':
            self.return_scores()
            self._c.start(self.songs[self.track_no][0])

    def set_bpm(self, bpm):
        """sets the bpm for the backend"""
        bpm = int(bpm)
        self.bpm = bpm
        tick_gap = bpm
        while tick_gap > 240:
            tick_gap /= 2
        if 100 > tick_gap != bpm:
            tick_gap *= 2
        tick_gap = 60000/tick_gap
        tick_gap /= 1000/30
        print(bpm, tick_gap)
        self.tick_gap = int(round(tick_gap))

    def get_song(self, num: int = -1):
        if num < 0:
            num = self.track_no
        return self.songs[num][0]

    def register(self):
        for menu in self.menus:
            self.menus[menu].register(self)

    def add_obstacle(self, x=256, y=256, rot=0, width=32):
        """for adding the obstacles"""
        self.obstacles.append(Obstacle(x, y, rot, width))
        self.obstacles[len(self.obstacles)-1].calculate_points()

    def rem_obstacle(self, pos=0):
        """for removing an obstacle"""
        self.obstacles.pop(pos)
        self.player.points += 1

    def check_rem(self):
        """for seeing if an obstacle needs to be removed"""
        for i in range(len(self.obstacles)-1):
            if self.obstacles[i].life <= 0:
                self.rem_obstacle(i)

    def calculate_collision(self):
        """all the collision calculations for checking if the player should be hurt"""
        player = self.player
        obstacles = self.obstacles
        player_left = player.pos_x-player.width//2
        player_right = player.pos_x+player.width//2
        player_top = player.pos_y-player.height//2
        player_bottom = player.pos_y+player.height//2
        for obstacle in obstacles:
            obstacle_left = obstacle.x-obstacle.width//2
            obstacle_right = obstacle.x+obstacle.width//2
            obstacle_top = obstacle.y-obstacle.width//2
            obstacle_bottom = obstacle.y+obstacle.width//2
            # dummy means invisible and uncollidable, start is for pregenning,
            # active is for hitable and hit is to stop multiple deaths
            if not obstacle.dummy and obstacle.start <= self.tick and not obstacle.active and not obstacle.hit:
                # first check if its upwards as it wont have an equation tied to it
                if obstacle.up:
                    if player_left < obstacle_right and player_right > obstacle_left:
                        player.lives -= 1
                        obstacle.hit = True
                # next if its sideways, same reason
                elif obstacle.right:
                    if player_top < obstacle_bottom and player_bottom > obstacle_top:
                        player.lives -= 1
                        obstacle.hit = True
                # now if its diagonally down
                elif obstacle.down:
                    if obstacle.get_y2(player_right) < player_bottom and player_top < obstacle.get_y1(player_left):
                        if player_left < obstacle.get_x2(player_top) and player_right > obstacle.get_x1(player_bottom):
                            player.lives -= 1
                            obstacle.hit = True
                # diagonally up
                else:
                    if obstacle.get_y1(player_right) < player_bottom and player_top < obstacle.get_y2(player_left):
                        if player_left < obstacle.get_x2(player_top) and player_right > obstacle.get_x1(player_bottom):
                            player.lives -= 1
                            obstacle.hit = True

    def obstacle_tick(self):
        """function called to check all of the obstacle hit stages. also controls the player boost"""
        self.tick += 1
        self.calculate_collision()
        for obstacle in self.obstacles:
            if obstacle.start > self.tick:
                continue
            if not obstacle.active:
                obstacle.life -= 1
            else:
                obstacle.active -= 1
        #print(self.tick, self.tick_gap)
        if self.tick % self.tick_gap == 0:
            self.create_obstacle(True, self.difficulties[self.difficulty])
        self.check_rem()
        if self.player.jump_off > 0:
            self.player.jump_off -= 0.1

    def create_obstacle(self, force=False, difficulty = 180):
        """obstacle randomisation process. Force is to ensure an obstacle is created"""
        creation_chance = randint(1, 20)
        if difficulty <= 0:
            difficulty = 1
        if creation_chance == 1 or force:
            width = randint(10, 64)
            x = randint(0 + width // 2, 512 - width // 2)
            rot = randint(1, difficulty)
            y = randint(0 + width // 2, 512 - width // 2)
            self.add_obstacle(x=x, width=width, rot=180/rot, y=y)

    def save_score(self, points, difficulty, song_name, player_name):
        #THIS FUNCTION
        print(points, difficulty, song_name, player_name)
        player_id = self.db.execute("select player_id from players where player_name = ?", [player_name]).fetchone()
        #FIRST TIME ROUND RETURNS NONE
        print(player_id)
        if not player_id:
            self.db.execute("insert into players values (?, ?)", [player_name, None])
            player_id = self.db.execute("select player_id from players where player_name = ?", [player_name]).fetchone()[0]
        #NOW RETURNS (None, )
        else:
            player_id = player_id[0]
        print(player_id)
        self.db.execute("insert into scores values(?, ?, ?, ?, ?)", [points, difficulty, song_name, player_id, None])
        self.conn.commit()

# Testing area
# test_obstacle = Obstacle()
# test_obstacle.calculate_points()
test_obstacle = Obstacle(rot=45)
test_obstacle.calculate_points()
# print(test_obstacle.points)
# print(test_obstacle.get_y1(127))
# print(test_obstacle.get_x1(362))
# test_obstacle = Obstacle(rot=90)
# test_obstacle.calculate_points()
test_obstacle = Obstacle(rot=-45)
test_obstacle.calculate_points()
# print(test_obstacle.points)
# print(test_obstacle.get_y1(127))
# print(test_obstacle.get_x1(362))
test_obstacle = Obstacle(rot=27.5)
test_obstacle.calculate_points()

# print(test_obstacle.points)
