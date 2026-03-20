import random
import math
import time
import numpy as np

class Dust:
    def change(positions, speeds, life_spans, colors, angle, amount):  # this will change direction and speed in paraler to it
        #filter = life_spans[:] <= 0
        chance = np.random.rand(amount) < 0.01
        angle[chance] = random.random() * 2 * math.pi

        positions[:, 0] += np.cos(angle) * speeds[:]
        positions[:, 1] += np.sin(angle) * speeds[:]

        return positions, speeds, life_spans, colors, angle


class Fireworks:
    def __init__(self):
        self.sparks=20

    def change(self, positions, speeds, life_spans, colors, angle, amount, exploded, explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle):
        explod = (positions[:, 1] <= explodey[:]) & (exploded[:] == 0)
        if explod.any():
            self.explode(positions, speeds, life_spans, colors, angle, amount, exploded ,explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle)
            exploded[explod] = 1

        if exploded.any() == 1:
            spark = Sparks()
            spark.change(exploded ,explodey, extra_particlesx, extra_particlesy)

        positions[:, 0] += np.cos(angle) * speeds[:]
        positions[:, 1] += np.sin(angle) * speeds[:]

        return positions, speeds, life_spans, colors, angle, amount, exploded, explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle


    def explode(self, positions, speeds, life_spans, colors, angle, amount, exploded ,explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle):
        filter = (positions[:, 1] <= explodey[:]) & (exploded[:] == 0)
        angle_part = (2 * math.pi) / amount
        extra_particlesx[filter] = positions[filter, 0]
        extra_particlesy[filter] = positions[filter, 1]
        extra_particles_angle[filter] = 0
        print("S")
#    def change(self):
#        if self.explode_y < self.y:
#            speed_change = [0, -1]
#            self.speed = [self.speed[0] + speed_change[0], self.speed[1] + speed_change[1]]
#            self.x = self.x + self.speed[0]
#            self.y = self.y + self.speed[1]
#
#        elif len(self.extra_particles) > 1:
#            for spark in self.extra_particles:
#                spark.change()
#
#        elif not self.exploded:
#            self.exploded = True
#            self.explode()
#
#        else:
#            self.life_span = 0
#        return self

#    def explode(self, amount=20):
#        angle_part = (2 * math.pi) / amount
#        for i in range(amount):
#           angle = angle_part * i
#           self.extra_particles.append(Sparks(self.x, self.y, 3, (250, 200, 200), angle, 20))


class Sparks:
    def __init__(self):
        pass

    def change(self, exploded ,explodey, extra_particlesx, extra_particlesy):
        speed_change = 0

        #self.speed = self.speed * self.resistance
        #self.dy, self.dx = self.dy * self.resistance, self.dx * self.resistance
        #self.dy += 0.03
        #self.x += self.dx
        #self.y += self.dy
        #self.fade()

        return

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

#made by rokrerum