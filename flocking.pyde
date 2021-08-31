# Winry/Tigrex, 8/30/2021
# Inspired by Daniel Shiffman from the Coding Train, which was itself inspired by
# Craig Reynold's paper about boids.
# This sketch will be a flocking system that uses a Boid class, and demonstrates
# the three concepts Craig outlined: Alignment, Cohesion, and Separation.
#
# Version comments:
# v0.00:  These version comments
# v0.0 :  Shell, new tab, Boid class
# v0.0 :  Alignment
# v0.0 :  Cohesion
# v0.0 :  Separation
# v0.0 :  Maybe refactor code into a Flock class and use quadtrees?


def setup():
    global boids
    colorMode(HSB, 360, 100, 100, 100)
    size(940, 1000)
    background(220, 79, 35) # this won't stay here long because it's a test.
    boids = []


def draw():
    global boids
    for boi
