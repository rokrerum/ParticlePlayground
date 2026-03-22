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

    def change(self, positions, speeds, life_spans, colors, angle, amount, exploded, explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle, extra_particles_colour):
        explod = (positions[:, 1] <= explodey[:]) & (exploded[:] == 0)
        if explod.any():
            self.explode(positions, speeds, life_spans, colors, angle, amount, exploded ,explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle)
            exploded[explod] = 1

        if exploded.any() == 1:
            spark = Sparks()
            life_spans, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle, extra_particles_colour = spark.change(life_spans, exploded, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle, extra_particles_colour)

        positions[:, 0] += np.cos(angle) * speeds[:]
        positions[:, 1] += np.sin(angle) * speeds[:]
        return positions, speeds, life_spans, colors, angle, amount, exploded, explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle


    def explode(self, positions, speeds, life_spans, colors, angle, amount, exploded ,explodey, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle):
        filter = (positions[:, 1] <= explodey[:]) & (exploded[:] == 0)
        angle_part = (2 * math.pi) / self.sparks
        extra_particlesx[filter] = positions[filter, 0:1]
        extra_particlesy[filter] = positions[filter, 1:2]
        extra_particles_angle[filter, :] = np.arange(self.sparks) * angle_part


class Sparks:
    def __init__(self):
        pass

    def change(self, life_spans, exploded, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle, extra_particles_colour):
        speed_change = 0

        exploded = exploded[:] == 1
        extra_particlesx[exploded, :] += np.cos(extra_particles_angle[exploded,:]) * 2
        extra_particlesy[exploded, :] += (np.sin(extra_particles_angle[exploded,:]) * 2) + 0.03
        extra_particles_colour[exploded, :] = abs(extra_particles_colour[exploded] - 1) #fadeing of  particles

        vanished = (extra_particles_colour == 0).all(axis=1) #checks if all numbers in row are 0
        life_spans[vanished] = 0

        return life_spans, extra_particlesx, extra_particlesy, extra_particles_speed, extra_particles_angle, extra_particles_colour


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