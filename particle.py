import random

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
        return self
