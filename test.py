import pygame
import sys
import math
import time

pygame.init()
pygame.font.init()

'''Colours'''
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (200, 200, 0)
blue = (0, 0, 255)
light_blue = (100, 150, 255)
dark_blue = (0, 10, 40)
green = (0, 175, 0)
light_green = (0, 255, 0)
red = (255, 0, 0)

'''Value of constant G'''
G = 6.673 * 10 ** -11

'''Display initialisation'''
'''Fullscreen causing the screen to be bigger than viewable -> will come back to later, rest of code coded
so that screen width and height can be any values and location of viewable objects is still accurate(centered)'''
screen = pygame.display.set_mode((1300, 600))
# ,pygame.FULLSCREEN
pygame.display.set_caption('Planetary Simulator')
screen.fill(green)
pygame.display.flip()

'''Gets Width and height of the screen'''
screenWidth = screen.get_width()
screenHeight = screen.get_height()

'''Width and height of screen divided by 2'''
screenWidth_d2 = int(screenWidth / 2)
screenHeight_d2 = int(screenHeight / 2)

# print('( x =',screenWidth, ', y =', screenHeight, ')')

clock = pygame.time.Clock()
clock.tick(30)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

planet_list = []

'''Planet class'''


class Planet:
    def __init__(self, x, y, r, m, colour, vx=0, vy=0, ax=0, ay=0):
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.colour = colour
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay


'''List of planets -> x & y accurate for all sizes of the screen using screenWidth_d2 and screenHeight_d2 to centre sun and planets'''


def create_class_planets(planet_list):
    sun = Planet(screenWidth_d2, screenHeight_d2, 50, 3000, yellow)
    planet_list.append(sun)

    mercury = Planet(screenWidth_d2 - 100, screenHeight_d2, 5, 20, red)
    planet_list.append(mercury)

    venus = Planet(screenWidth_d2 - 150, screenHeight_d2, 10, 20, red)
    planet_list.append(venus)

    earth = Planet(350, screenHeight_d2, 15, 50, green)
    # planet_list.append(earth)

    mars = Planet(300, screenHeight_d2, 20, 20, red)
    # planet_list.append(mars)

    jupiter = Planet(250, screenHeight_d2, 20, 20, red)
    # planet_list.append(jupiter)

    saturn = Planet(250, screenHeight_d2, 20, 20, red)
    # planet_list.append(saturn)

    uranus = Planet(150, screenHeight_d2, 10, 20, red)
    # planet_list.append(uranus)

    neptune = Planet(100, screenHeight_d2, 10, 20, red)
    # planet_list.append(neptune)

    pluto = Planet(50, screenHeight_d2, 5, 20, red)
    # planet_list.append(pluto)


create_class_planets(planet_list)

# print(planet_list)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main():
    #clock.tick(30)
    quit = False
    x1 = int(screenWidth / 10)
    y1 = int(screenHeight - 450)
    x2 = int(screenWidth / 10)
    y2 = int(screenHeight - 400)
    x3 = 10
    y3 = int(screenHeight - 25)

    font1 = pygame.font.SysFont('System', 80)
    font2 = pygame.font.SysFont('System', 45)
    font3 = pygame.font.SysFont('System', 30)
    text_title = font1.render('PLANETARY SIMULATOR', True, white)
    text_author = font2.render('BY DYLAN PIERCY', True, white)
    text_click = font3.render('Click anywhere to continue...', True, white)

    screen.blit(text_title, (x1, y1))
    screen.blit(text_author, (x2, y2))
    screen.blit(text_click, (x3, y3))

    # mousePosition = pygame.mouse.get_pos()
    # click = pygame.mouse.get_pressed()

    # if click[0] == 1 and action != None:
    #   welcome_screen()
    #time.sleep(0.001)
    button()


def welcome_screen():
    screen.fill(dark_blue)

    x1 = int((screenWidth / 2) - 75)
    y1 = int(screenHeight - 250)
    x2 = int(screenWidth / 10)
    y2 = int(screenHeight - 450)
    x3 = int(screenWidth / 10)
    y3 = int(screenHeight - 400)

    font1 = pygame.font.SysFont('System', 65)
    font2 = pygame.font.SysFont('System', 45)
    font3 = pygame.font.SysFont('System', 35)
    text_welcome = font1.render('WELCOME', True, white)
    text_button = font2.render('Continue', True, black)

    file = open("welcome.txt", "r")
    # Lines = file.readlines()
    # count = 0
    # for line in Lines:
    #     print("Line{}: {}".format(count, line.strip()))
    text_welcome_file = font3.render(file.read(), True, white)

    tx = int(x1 + text_button.get_rect().width / 2) - 60
    ty = int(y1 + text_button.get_rect().height // 2) + 8

    mousePosition = pygame.mouse.get_pos()

    screen.blit(text_welcome, (x2, y2))
    screen.blit(text_welcome_file, (x3, y3))

    # if x1+150 > mousePosition[0] > x1 and y1+75 > mousePosition[1] > y1:
    #  pygame.draw.rect(screen, light_green, (x1, y1, 150, 75))
    #   screen.blit(text_button,(tx,ty))
    # else:
    #     pygame.draw.rect(screen, green, (x1, y1, 150, 75))
    #      screen.blit(text_button,(tx,ty))
    #   pygame.display.update()

    # for event in pygame.event.get():
    #    if event.type == pygame.MOUSEBUTTONDOWN:
    #       if x1+150 > mousePosition[0] > x1 and y1+75 > mousePosition[1] > y1:
    #          difficulty_screen()

    return True


def difficulty_screen():
    screen.fill(dark_blue)
    quit = True

    x1 = int(screenWidth / 10)
    y1 = int(screenHeight - 500)
    x2 = int(screenWidth / 10)
    y2 = int(screenHeight - 400)

    font1 = pygame.font.SysFont('System', 65)
    font2 = pygame.font.SysFont('System', 45)
    font3 = pygame.font.SysFont('System', 35)

    text_skill = font1.render('SKILL LEVEL', True, white)
    simplistic_button = font2.render('Simplistic', True, black)
    advanced_button = font2.render('Advanced', True, black)

    file = open("skill.txt", "r")
    text_skill_file = font3.render(file.read(), True, white)

    screen.blit(text_skill, (x1, y1))
    screen.blit(text_skill_file, (x2, y2))

    mode_screen()


def mode_screen():
    screen.fill(dark_blue)

    x1 = int(screenWidth / 10)
    y1 = int(screenHeight - 500)
    x2 = int(screenWidth / 10)
    y2 = int(screenHeight - 400)

    font1 = pygame.font.SysFont('System', 65)
    font2 = pygame.font.SysFont('System', 45)
    font3 = pygame.font.SysFont('System', 35)

    text_skill = font1.render('MODE TYPE', True, white)
    simplistic_button = font2.render('Simplistic', True, black)
    advanced_button = font2.render('Advanced', True, black)

    file = open("mode.txt", "r")
    text_skill_file = font3.render(file.read(), True, white)

    screen.blit(text_mode, (x1, y1))
    screen.blit(text_mode_file, (x2, y2))
    pass


def button():
    #while True:
        #clock.tick(30)
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screenWidth > mousePosition[0] > 0 and screenHeight > mousePosition[1] > 0:
                    welcome_screen()
        #main()


def button2():
    while True:
        clock.tick(30)
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screenWidth > mousePosition[0] > 0 and screenHeight > mousePosition[1] > 0:
                    difficulty_screen()


main()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'''Plots planets in list'''


def plot_planets(planet_list):
    for planet in planet_list:
        pygame.draw.circle(screen, blue, (planet.x, planet.y), planet.r)
    pygame.display.update()


'''Calculates the forces, acceleration and angles of bodies from one another'''


def calculate_planet_forces(planet_list):
    for i in range(0, len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            planet_1 = planet_list[i]
            planet_2 = planet_list[j]

            '''F = G * m1 * m2 /D^2 -> Where D = the distance between the planets'''

            D = math.sqrt(((planet_2.x - planet_1.x) ** 2) + ((planet_2.y - planet_1.y) ** 2))
            F = G * ((planet_1.m * planet_2.m) / D ** 2)

            print('Distance Between Planets == ', D)
            print('Force Between Planets == ', F)

            '''a = F / m ---> aceleration towards eachother'''
            planet_1_a = F / planet_1.m
            planet_2_a = F / planet_2.m

            print('a1 = ', planet_1_a, 'a2 = ', planet_2_a)

            '''Angle of the distance between the planets from normal'''
            theta = math.atan((planet_2.y - planet_1.y) / (planet_2.x - planet_1.x))
            if (planet_2.x - planet_1.x) < 0:
                angle = 90 + theta
            else:
                angle = 90 - theta

            print('Angle Of Distance', angle, 'degrees')
            '''not accurate for when planet_2.y < planet_1.y'''

            planet_ax1 = (planet_1_a / ((planet_2.y - planet_1.y) + (planet_2.x - planet_1.x))) * (
                        planet_2.x - planet_1.x)
            planet_ax2 = math.cos(angle) * planet_1_a

            print('ax1 --- ', planet_ax1)
            print('ax2 --- ', planet_ax2)
            print('')

            # planet_1.ax += math.cos(angle) * planet_1_a
            # planet_1.ay += math.sin(angle) * planet_1_a
            # planet_2.ax += math.cos(angle + math.pi) * planet_2_a
            # planet_2.ay += math.sin(angle + math.pi) * planet_2_a

    # def replot_planets(planet_list)

    '''Collisions of bodies'''
    if D <= planet_1.r + planet_2.r:
        planet_list.pop(planet_1)
        planet_list.pop(planet_2)
        new_planet = Planet((planet_2.x - planet_1.x) / 2,
                            (planet_2.y - planet_1.y) / 2,
                            math.sqrt(((math.pi * planet_1.r ** 2) + (math.pi * planet_2.r ** 2)) / math.pi),
                            planet_1.m + planet_2.m,
                            red)


# calculate_planet_forces(planet_list)
# plot_planets(planet_list)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'''Quit button -> x & y of rectangle and text accurate for all sizes of the screen'''
while quit:
    '''x & y of rectangle'''
    x = screenWidth - 100
    y = screenHeight - 50
    # print(x, y)

    font = pygame.font.SysFont('System', 40)
    text = font.render('Quit', True, black)

    '''x & y of text'''
    tx = int(screenWidth - ((100 / 2) + (text.get_rect().width / 2)))
    ty = int(screenHeight - ((50 / 2) + ((text.get_rect().height) / 2)))
    # print(tx, ty)

    mousePosition = pygame.mouse.get_pos()

    '''Draws rectangle for button and displays text on top of it.
    If mousePosition is in range it changes colour to demonstrate mouse is over the button'''
    if x + 100 > mousePosition[0] > x and y + 50 > mousePosition[1] > y:
        pygame.draw.rect(screen, red, (x, y, 100, 50))
        screen.blit(text, (tx, ty))
    else:
        pygame.draw.rect(screen, blue, (x, y, 100, 50))
        screen.blit(text, (tx, ty))
    pygame.display.update()

    '''If user clicks on the button it closes pygame and shell'''
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x + 100 > mousePosition[0] > x and y + 50 > mousePosition[1] > y:
                pygame.quit()
                exit()

'''
collisions of planets:
if d < r1 + r2 then
d -> distance between planet centres
r1 & r2 = radius of both planets
larger planet mass = m1 + m2
remove smaller planet
set new orbit, velocity and acceleration
set new radius based off of mass/volume/density
- all planets have same modeled density

equation v = SQRT(G * Mcentral / R),
the mass of the central body and the radius of the orbit affect orbital speed
G = constant = 6.673 x 10^-11 N•m2/kg2
Acceleration = resultant force divided by mass
'''
