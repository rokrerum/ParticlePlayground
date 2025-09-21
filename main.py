import pygame
import random
import time
from pygame.locals import *
import sys
import pygame_gui
import particle

pygame.init()


class MainWindow:
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.menu = "options"
        self.input_boxes = []
        self.input_buttons = []
        self.display = pygame.display.set_mode((self.width,self.height))
        self.font = pygame.font.SysFont(None, 20)
        

    def draw(self, particles):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, self.width - 200, self.height))
        for i in particles:
            pygame.draw.rect(self.display, (22, 200, 100), (i.x, i.y, 2, 2))
           
        pygame.display.update()  
   
   
    def particle_menu(self, partile_types):
        button = pygame_gui.button
        pygame.draw.rect(self.display, (20, 20, 80), (self.width - 200, 0, 200, self.height))
        for ind, particle in enumerate(partile_types):
            ind += 1
            self.input_buttons.append(button((self.width - 200, 20 * ind, 20, 20), particle, self.font, (22, 160, 160), self.display))
            self.input_buttons[-1].add_button()


    def setings_menu(self): ## need to add menu button and restart button
        running = True
        Gui = pygame_gui.Gui
        pygame.draw.rect(self.display, (20, 20, 80), (self.width - 200, 0, 200, self.height))
        Gui.draw_text(self.width - 200, 55, "amount", self.font, (22, 160, 160), self.display)
        input_box1 = pygame_gui.InputBox(self.width - 200, 70, 120, 20, "amount")

        Gui.draw_text(self.width - 200, 95, "life span", self.font, (22, 160, 160), self.display)
        input_box2 = pygame_gui.InputBox(self.width - 200, 110, 120, 20, "life span")

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



spawn_area = \
    {
    "xstart": 200,
    "xend": 500,
    "ystart": 200,
    "yend": 500,
    }

particle_info = \
    {
    "amount": 1000,
    "speed": [0, 0],
    "color": (22, 200, 100),
    "direction": None,
    "type": "dust",
    "life_span": 20
    }
    
partile_types = [
    "dust",
    "fireworks"
]
       
particle_data = particle.Particle
mainWindow = MainWindow(900,600)
mainWindow.particle_menu(partile_types)
particles = []
input_boxes = mainWindow.input_boxes
input_buttons = mainWindow.input_buttons
display = mainWindow.display

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        for box in input_boxes:
            box.handle_event(event)
       
    for ind, particle in enumerate(particles):
        if particle.life_span <= time.time():
            particles.pop(ind)
        else:
            particles[ind] = particle.change()
   
    for box in input_boxes:
        box.draw(display)
        if box.submitted is not None:
            if box.var_name == "amount":
                particle_info["amount"] = int(box.submitted)
                
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
    
    for button in input_buttons:
        pass

   
    while len(particles) < particle_info["amount"]:
        particles.append(particle_data(random.randint(spawn_area["xstart"], spawn_area["xend"]), random.randint(spawn_area["ystart"], spawn_area["yend"]),\
            particle_info["speed"], particle_info["color"],\
           [random.choice(["n", "s"]), random.choice(["w", "e"])],\
           particle_info["type"], int(time.time()) + particle_info["life_span"]))

    time.sleep(0.09)
    mainWindow.draw(particles)
    pygame.display.update()
