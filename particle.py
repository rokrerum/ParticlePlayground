import random
import math
import time
import numpy as np

class ParticleData:
    def __init__(self, size = 1):
        self.positions = np.zeros((size, 2))  # amount of particles, x i y
        self.speeds = np.zeros(size)
        self.life_spans = np.zeros(size)
        self.colors = np.zeros((size, 3))  # r, g, b
        self.angle = np.zeros(size)
        self.exploded = np.full(size, 0)
        self.explodey = np.zeros(size)  # on what y
        self.extra_particlesx = np.zeros((size, 20))
        self.extra_particlesy = np.zeros((size, 20))
        self.extra_particles_speed = np.zeros((size, 20))
        self.extra_particles_angle = np.zeros((size, 20))
        self.extra_particles_colour = np.zeros((size, 3))

    def size_change(self, size):
        self.positions = np.zeros((size, 2))  # amount of particles, x i y
        self.speeds = np.zeros(size)
        self.life_spans = np.zeros(size)
        self.colors = np.zeros((size, 3))  # r, g, b
        self.angle = np.zeros(size)

    def firework_size_change(self, size):
        self.exploded = np.full(size, 0)
        self.explodey = np.zeros(size)  # on what y
        self.extra_particlesx = np.zeros((size, 20))
        self.extra_particlesy = np.zeros((size, 20))
        self.extra_particles_speed = np.zeros((size, 20))
        self.extra_particles_angle = np.zeros((size, 20))
        self.extra_particles_colour = np.zeros((size, 3))

    def create_particle_dust(self, size):
        filter = self.life_spans[:] <= 0
        self.life_spans[filter] = 8
        self.positions[filter, 0] = np.random.randint(0, 400, size)
        self.positions[filter, 1] = np.random.randint(0, 400, size)
        self.speeds[filter] = 1
        self.angle[filter] = np.random.random(size) * (2 * math.pi)
        self.colors[filter, 0] = 22
        self.colors[filter, 1] = 222
        self.colors[filter, 2] = 222

    def create_particle_firework(self):
        filter = self.life_spans[:] <= 0
        self.life_spans[filter] = 8
        self.positions[filter, 0] = np.random.randint(100, 500, filter.sum())
        self.positions[filter, 1] = 500
        self.speeds[filter] = 1
        self.angle[filter] = math.pi * 1.5
        self.colors[filter, 0] = 22
        self.colors[filter, 1] = 222
        self.colors[filter, 2] = 222
        self.exploded[filter] = 0
        self.explodey[filter] = np.random.randint(100, 300, filter.sum())
        self.extra_particlesx[filter, :] = 0
        self.extra_particlesy[filter, :] = 0
        self.extra_particles_speed[filter] = 1
        self.extra_particles_angle[filter] = 0
        self.extra_particles_colour[filter, :] = 222


class Dust:
    def change(particles, size):  # this will change direction and speed in paraler to it
        #filter = life_spans[:] <= 0
        chance = np.random.rand(size) < 0.01
        particles.angle[chance] = random.random() * 2 * math.pi

        particles.positions[:, 0] += np.cos(particles.angle) * particles.speeds[:]
        particles.positions[:, 1] += np.sin(particles.angle) * particles.speeds[:]

        return particles


class Fireworks:
    def __init__(self):
        self.sparks=20

    def change(self, particles, size):
        exploded_check = (particles.positions[:, 1] <= particles.explodey[:]) & (particles.exploded[:] == 0)
        if exploded_check.any():
            self.explode(particles, size)
            particles.exploded[exploded_check] = 1

        if particles.exploded.any() == 1:
            spark = Sparks()
            particles = spark.change(particles, size)

        particles.positions[:, 0] += np.cos(particles.angle) * particles.speeds[:]
        particles.positions[:, 1] += np.sin(particles.angle) * particles.speeds[:]
        return particles


    def explode(self, particles, size):
        filter = (particles.positions[:, 1] <= particles.explodey[:]) & (particles.exploded[:] == 0)
        angle_part = (2 * math.pi) / self.sparks
        particles.extra_particlesx[filter] = particles.positions[filter, 0:1]
        particles.extra_particlesy[filter] = particles.positions[filter, 1:2]
        particles.extra_particles_angle[filter, :] = np.arange(self.sparks) * angle_part


class Sparks:
    def __init__(self):
        pass

    def change(self, particles, size):
        exploded = particles.exploded[:] == 1
        particles.extra_particlesx[exploded, :] += np.cos(particles.extra_particles_angle[exploded,:]) * 2
        particles.extra_particlesy[exploded, :] += (np.sin(particles.extra_particles_angle[exploded,:]) * 2) + 0.03
        particles.extra_particles_colour[exploded, :] = abs(particles.extra_particles_colour[exploded] - 1) #fadeing of  particles

        vanished = (particles.extra_particles_colour == 0).all(axis=1) #checks if all numbers in row are 0 and if they are particle is not visible
        particles.life_spans[vanished] = 0

        return particles


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