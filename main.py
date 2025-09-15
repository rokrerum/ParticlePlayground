import pygame
import random
import time
from pygame.locals import *
import sys

pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class MainWindow:
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.menu = "options"
        self.input_boxes = []
        self.display=pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Caption")
    
    
    def draw(self, particles):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, self.width - 200, self.height))
        for i in particles:
            pygame.draw.rect(self.display, (22, 200, 100), (i.x, i.y, 2, 2))
            
        pygame.display.update()   
    
    
    font = pygame.font.SysFont(None, 20)
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        
    
    def setings_menu(self):
        
        running = True
        pygame.draw.rect(self.display, (20, 20, 80), (self.width - 200, 0, 200, self.height))
        input_box1 = InputBox(self.width - 200, 100, 140, 32)
        input_box2 = InputBox(self.width - 200, 300, 140, 32)
        
        self.input_boxes = [input_box1, input_box2]
        
        
    def particle_menu(self):
        running = True
        while running:
            self.display.fill((0,0,0))
            
            
    def menu_interactions(self):
        pass


class Particle:
    def __init__(self, x, y, speed, color, direction, type_, life_span):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.direction = direction
        self.type = type_
        self.life_span = life_span
    
    
    def change(self): # this will change direction and speed in paraler to it 
        if self.type == "dust": #this is for changing diretctin of mevment of particles
            rand = random.randint(0, 10)
            if rand == 10:
                self.direction = [random.choice(["n", "s"]), random.choice(["w", "e"])] 
            
            speed_change = [0, 0]
            if self.direction[0] == "n":
                speed_change[0] = random.randint(-2, -1) if self.speed[0] >= 3 else random.randint(1, 2)
            else:
                speed_change[0] = random.randint(1, 2) if self.speed[0] <= -3 else random.randint(-2, -1)
            
            if self.direction[1] == "w":
                speed_change[1] = random.randint(-2, -1) if self.speed[1] >= 3 else random.randint(1, 2)
            else:
                speed_change[1] = random.randint(1, 2) if self.speed[1] <= -3 else random.randint(-2, -1)
            
        self.speed = [self.speed[0] + speed_change[0], self.speed[1] + speed_change[1]]
        self.x = self.x + self.speed[0]
        self.y = self.y + self.speed[1]
        return particle
        
     
     
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)


    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        # Blit the text.
        pygame.draw.rect(screen, (20, 20, 80), self.rect,)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        
        pygame.draw.rect(screen, self.color, self.rect, 2)

   
        
particle_data = Particle
mainWindow = MainWindow(900,600)
mainWindow.setings_menu()
particles = []
input_boxes = mainWindow.input_boxes
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
    
    while len(particles) < 100000:
        particles.append(Particle(random.randint(200,400), random.randint(200,400), [0, 0], "white", [random.choice(["n", "s"]), random.choice(["w", "e"])], "dust", int(time.time()) + 20))

    mainWindow.draw(particles)
    pygame.display.update()
