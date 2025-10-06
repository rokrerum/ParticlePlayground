import random
import math


class Dust:
    def __init__(self, x, y, speed, color, direction, life_span):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.direction = direction
        self.life_span = life_span
        self.extra_particles = []
   
   
    def change(self): # this will change direction and speed in paraler to it
        #this is for changing diretctin of mevment of particles
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
        return self
    
    
    
class Fireworks:
    def __init__(self, x, y, speed, color, direction, life_span):
        self.x = x
        self.y = y
        self.speed = [0, -1]
        self.color = color
        self.direction = direction
        self.life_span = life_span
        self.exploded = False
        self.explode_y = int(random.randint(50, 200))
        self.extra_particles = []
        
        
    def change(self):
        if self.explode_y < self.y:
            rand = random.randint(0, 10)
            if rand == 10:
                direction_firework = [random.choice("n"), random.choice(["w", "e"])]
            speed_change = [0, -1]
            self.speed = [self.speed[0] + speed_change[0], self.speed[1] + speed_change[1]]
            self.x = self.x + self.speed[0]
            self.y = self.y + self.speed[1]
    
        elif len(self.extra_particles) > 1:
            for spark in self.extra_particles:
                spark.change()
        
        elif not self.exploded:
            self.exploded = True
            self.explode()
        
        else:
            self.life_span = 0
        return self
    
    
    def explode(self, amount = 20):
        angle_part = (2*math.pi) / amount
        for i in range(amount):
            angle = angle_part * i
            self.extra_particles.append(Sparks(self.x, self.y, 3, (200, 200, 200), angle, 20))
    
    
class Sparks:
    def __init__(self, x, y, speed, color, angle, life_span):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.angle = angle
        self.life_span = int(2)
        self.extra_particles = []
        
        
    def change(self):
        speed_change = 0
        
        self.speed = self.speed + speed_change
        dx = math.cos(self.angle) * self.speed
        dy = (math.sin(self.angle) * self.speed) 
        self.x += dx
        self.y += dy 
        #self.fade()
        
        return self
    
    
    def fade(self): # need to add removing particle after it fates
        self.color = (abs(self.color[0] - 2), abs(self.color[1] - 2), abs(self.color[2] - 2))
        
        if self.color[0] == 0 and self.color[1] == 0 and self.color[2] == 0:
            self.life_span = 0
        
