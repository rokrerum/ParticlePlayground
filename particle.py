import random
import math
import time


class Particle:  # base class for all porticles
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.color = (0, 0, 0)
        self.life_span = 0
        self.extra_particles = []

    def move_angle(self):
        self.speed = self.speed * self.resistance
        self.dy, self.dx = self.dy * self.resistance, self.dx * self.resistance

    def gravity(self):
        self.dy += 0.03


class Dust:
    def __init__(self, x, y, speed, color, direction, life_span):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.direction = direction
        self.life_span = life_span
        self.extra_particles = []

    def change(self):  # this will change direction and speed in paraler to it
        # this is for changing diretctin of mevment of particles
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
    def __init__(self, x, y, speed, color, life_span):
        self.x = x
        self.y = y
        self.speed = [0, -1]
        self.color = color
        self.life_span = life_span
        self.exploded = False
        self.explode_y = int(random.randint(50, 200))
        self.extra_particles = []

    def change(self):
        if self.explode_y < self.y:
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

    def explode(self, amount=20):
        angle_part = (2 * math.pi) / amount
        for i in range(amount):
            angle = angle_part * i
            self.extra_particles.append(Sparks(self.x, self.y, 3, (250, 200, 200), angle, 20))


class Sparks:
    def __init__(self, x, y, speed, color, angle, life_span):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.angle = angle
        self.life_span = int(2)
        self.resistance = 0.99
        self.extra_particles = []
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

    def change(self):
        speed_change = 0

        self.speed = self.speed * self.resistance
        self.dy, self.dx = self.dy * self.resistance, self.dx * self.resistance
        self.dy += 0.03
        self.x += self.dx
        self.y += self.dy
        self.fade()

        return self

    def fade(self):
        self.color = (abs(self.color[0] - 1), abs(self.color[1] - 1), abs(self.color[2] - 1))

        if self.color[0] == 0 and self.color[1] == 0 and self.color[2] == 0:
            self.life_span = 0


class Snow:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = 1
        self.color = color
        self.angle = random.uniform(math.pi * 0.3, math.pi * 0.6)
        self.extra_particles = []
        self.life_span = int(time.time()) + 500
        self.dx = 0
        self.dy = 0

    def change(self):
        # speed_change = 0
        rand = random.randint(0, 100)
        if rand == 100:
            self.angle = random.uniform(math.pi * 0.2, math.pi * 0.8)
            print(self.angle)

        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        self.x += self.dx
        self.y += self.dy

        return self
