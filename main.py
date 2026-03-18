import pygame
import random
import time
from pygame.locals import *
import sys
import pygame_gui
import particle
import keyboard
import json
import numpy as np

pygame.init()
clock = pygame.time.Clock()

class MainWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.menu = "particle_selection"
        self.input_boxes = []
        self.input_buttons = []
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, particles):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, self.width - 200, self.height))
        for particle_ in particles:
            if particle_ is not None:
                if len(particle_.extra_particles) == 0:
                    pygame.draw.rect(self.display, particle_.color, (particle_.x, particle_.y, 2, 2))
                else:
                    for p in particle_.extra_particles:
                        pygame.draw.rect(self.display, p.color, (p.x, p.y, 2, 2))

        pygame.display.update()

    def particle_menu(self, partile_types):
        button = pygame_gui.button
        pygame.draw.rect(self.display, (20, 20, 80), (self.width - 200, 0, 200, self.height))
        for ind, particle in enumerate(partile_types):
            ind += 1
            self.input_buttons.append(
                button((self.width - 200, 20 * ind, 60, 20), particle, self.font, (22, 160, 160), self.display))
            self.input_buttons[-1].add_button()

    def setings_menu(self):  ## need to add menu button and restart button
        button = pygame_gui.button
        running = True
        Gui = pygame_gui.Gui
        pygame.draw.rect(self.display, (20, 20, 80), (self.width - 200, 0, 200, self.height))
        self.input_buttons.append(
            button((self.width - 200, 20, 60, 20), "particles", self.font, (22, 160, 160), self.display))
        self.input_buttons[-1].add_button()

        self.input_buttons.append(
            button((self.width - 100, 20, 60, 20), "remove particles", self.font, (22, 160, 160), self.display))
        self.input_buttons[-1].add_button()

        self.input_buttons.append(
            button((self.width - 200, 50, 60, 20), "reset settings", self.font, (200, 160, 160), self.display))
        self.input_buttons[-1].add_button()

        self.input_buttons.append(
            button((self.width - 100, 50, 60, 20), "save settings", self.font, (22, 160, 160), self.display))
        self.input_buttons[-1].add_button()

        Gui.draw_text(self.width - 200, 75, "amount", self.font, (22, 160, 160), self.display)
        input_box1 = pygame_gui.InputBox(self.width - 200, 88, 120, 20, "amount")

        Gui.draw_text(self.width - 200, 112, "life span", self.font, (22, 160, 160), self.display)
        input_box2 = pygame_gui.InputBox(self.width - 200, 126, 120, 20, "life span")

        Gui.draw_text(self.width - 200, 150, "spawn area", self.font, (22, 160, 160), self.display)

        Gui.draw_text(self.width - 160, 165, "x", self.font, (22, 160, 160), self.display)
        input_box3 = pygame_gui.InputBox(self.width - 160, 180, 40, 20, "xstart")
        input_box4 = pygame_gui.InputBox(self.width - 160, 210, 40, 20, "xend")

        Gui.draw_text(self.width - 100, 165, "y", self.font, (22, 160, 160), self.display)
        input_box5 = pygame_gui.InputBox(self.width - 100, 180, 40, 20, "ystart")
        input_box6 = pygame_gui.InputBox(self.width - 100, 210, 40, 20, "yend")

        Gui.draw_text(self.width - 200, 180, "from", self.font, (22, 160, 160), self.display)
        Gui.draw_text(self.width - 200, 210, "to", self.font, (22, 160, 160), self.display)

        self.input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5, input_box6]

    def menu_interactions(self):
        pass

def size_change(size):
    positions = np.zeros((size, 2))  # amount of particles, x i y
    speeds = np.zeros((size, 2))
    life_spans = np.zeros(size)
    colors = np.zeros((size, 3))  # r, g, b
    exploded = np.zeros((size, 2))
    angle = np.zeros((size, 2))
    extra_particlesx = np.zeros((size, 20))
    extra_particlesy = np.zeros((size, 20))
    extra_particles_speed = np.zeros((size, 20))
    extra_particles_ang = np.zeros((size, 20)) #angle
    return positions, speeds, life_spans, colors, exploded, angle

def info_change(particle, ind):
    positions[ind] = particle.x, particle.y
    speeds[ind] = particle.speed
    life_spans[ind] = particle.life_span
    colors[ind] = particle.color
    #extra_particles[ind] = particle.extra_particles
    if particle_type == "fireworks":
        exploded[ind] = particle.exploded, particle.explode_y
        angle[ind] = particle.dy, particle.dx


particle_type = "dust"
particle_info = {}
spawn_area = {}

partile_types = [
    "dust",
    "fireworks",
    "snow"
]

mainWindow = MainWindow(900, 600)
mainWindow.particle_menu(partile_types)
input_boxes = mainWindow.input_boxes
input_buttons = mainWindow.input_buttons
display = mainWindow.display
time_ = 0
stopped = False
particles = []
global positions  # amount of particles, x i y
global speeds
global life_spans
global colors  # r, g, b
global extra_particles
global exploded
global angle


data_file = "user_settings.json" #name of file
data = json.loads(open(data_file).read()) #loading data form files

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        for box in input_boxes:
            box.handle_event(event)

        for button in input_buttons:  # this is handler for buttons for operating eavents of buttons
            button_action = button.button_press(event)
            if button_action:
                if button_action in ["dust", "fireworks", "snow"]:
                    mainWindow.input_buttons = []
                    if button_action == "dust":
                        particle_type = "dust"
                        mainWindow.setings_menu()

                    elif button_action == "fireworks":
                        particle_type = "fireworks"
                        mainWindow.setings_menu()

                    elif button_action == "snow":
                        particle_type = "snow"
                        mainWindow.setings_menu()

                    mainWindow.menu = "particle_menu"
                    input_buttons = mainWindow.input_buttons
                    input_boxes = mainWindow.input_boxes  # name of file
                    file = json.loads(open("user_settings.json").read())  # loading data form files

                    for preset in file: # loads a info of particles form file
                        if preset.get("type") == particle_type:
                            particle_info = preset["info"]
                            spawn_area = preset["spawn_area"]
                    particles = np.empty(particle_info["amount"], dtype=object)


                elif button_action in ["remove particles", "particles", "save settings", "reset settings"]:
                    if button_action == "remove particles":
                        particles = np.empty(particle_info["amount"], dtype=object)

                    elif button_action == "particles":
                        mainWindow.menu = "particle_selection"
                        mainWindow.input_buttons = []
                        mainWindow.input_boxes = []
                        mainWindow.particle_menu(partile_types)
                        input_boxes = mainWindow.input_boxes
                        input_buttons = mainWindow.input_buttons

                    elif button_action == "save settings":
                        with open("user_settings.json", "r") as f:
                            file = json.load(f)

                        for data in range(len(file)):
                            if file[data]["type"] == particle_type:
                                file[data]["info"] = particle_info
                                file[data]["spawn_area"] = spawn_area

                        with open("user_settings.json", "w") as f:
                            json.dump(file, f)


                    elif button_action == "reset settings":
                        data_file = "default_settings.json"
                        data = json.loads(open(data_file).read())
                        for preset in data:  # loads a info of particles form file
                            if preset.get("type") == particle_type:
                                particle_info = preset["info"]
                                particle_type = preset.get("type")
                                spawn_area = preset["spawn_area"]


    if keyboard.is_pressed(" "):  # this give user ability to stop simulaton
        stopped = not stopped
        time.sleep(0.2)


    if mainWindow.menu != "particle_selection":  # this is for adding particle and input boxes in simulation
        #need to add varible and if for change if anything changed
        for box in input_boxes:
            box.draw(display)
            if box.submitted is not None:  # this checks if any value was change in input boxes
                if box.var_name == "amount":
                    particle_info["amount"] = int(box.submitted)
                    particles = np.empty(particle_info["amount"], dtype=object)
                    pozycja, predkosci, life_spans, kolory, exploded, angle = size_change(100)

                elif box.var_name == "life span":
                    particle_info["life_span"] = int(box.submitted)

                elif box.var_name == "xstart":
                    spawn_area["xstart"] = int(box.submitted)

                elif box.var_name == "xend":
                    spawn_area["xend"] = int(box.submitted)

                elif box.var_name == "ystart":
                    spawn_area["ystart"] = int(box.submitted)

                elif box.var_name == "yend":
                    spawn_area["yend"] = int(box.submitted)
                box.submitted = None #removes value form submitted so this will stop changing the value over and over

        if not stopped: #adding particles
            for ind, particle_ in enumerate(particles):
                if particle_ == None or particle_.life_span <= time.time():
                    if particle_type == "dust":
                        particle_data = particle.Dust
                        particle_selected = (particle_data(random.randint(spawn_area["xstart"], spawn_area["xend"]), random.randint(spawn_area["ystart"], spawn_area["yend"]), particle_info["speed"], particle_info["color"], [random.choice(["n", "s"]), random.choice(["w", "e"])], int(time.time()) + particle_info["life_span"]))

                    elif particle_type == "fireworks":
                        particle_data = particle.Fireworks
                        particle_selected = particle_data(random.randint(spawn_area["xstart"], spawn_area["xend"]),mainWindow.height,particle_info["speed"], particle_info["color"],int(time.time()) + particle_info["life_span"])

                    elif particle_type == "snow": # to change
                        particle_data = particle.Snow
                        if (particle_ is None and time.time() > time_):
                            time_ = time.time() + (5 / particle_info["amount"])
                            particles[ind] = (particle_data(random.randint(spawn_area["xstart"], spawn_area["xend"]), 0, particle_info["speed"], particle_info["color"]))

                    particles[ind] = particle_selected

                else:
                    particles[ind] = particle_.change()

    clock.tick(60)
    mainWindow.draw(particles)
    pygame.display.update()

#made by rokrerum