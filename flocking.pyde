# Winry/Tigrex, 8/30/2021
# Inspired by Daniel Shiffman from the Coding Train, which was itself inspired by
# Craig Reynold's paper about boids.
# This sketch will be a flocking system that uses a Boid class, and demonstrates
# the three concepts Craig outlined: Alignment, Cohesion, and Separation.
#
# Version comments:
# v0.00:  These version comments
# v0.01:  Shell, new tab, Boid class
# v0.02:  Alignment
# v0.03:  Cohesion
# v0.04:  Separation
# v0.05:  Maybe refactor code into a Flock class and use quadtrees?
from Boid import * # an asterisk imports everything in a file or library


def setup():
    global boids
    colorMode(HSB, 360, 100, 100, 100)
    size(640, 360)   
    # size(640, 360)
    # background(220, 79, 35) # this won't stay here long because it's a test.
    boids = []
    for i in range(100):
        boids.append(Boid(random(width), random(height)))


def draw():
    global boids
    background(220, 79, 35)
    gravity = PVector(0, 0.1)
    for boid in boids:
        target = PVector(mouseX, mouseY)
        # desired_velocity = PVector.sub(target, boid.pos)
        # boid.apply_force(boid.velocity_seek(desired_velocity))
        boid.flock(boids)
    
    for boid in boids:
        # boid.apply_force(gravity)
        boid.show()
        boid.edges()
        boid.update()
    
    fill(0, 0, 100)
    text("{:.2f}".format(frameRate), 10, 10)
