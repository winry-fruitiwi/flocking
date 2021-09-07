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
# v0.05:  Move flock function to a different loop
# v0.06:  Refactored alignment
# v0.07:  Add all three functions

from Boid import * # an asterisk imports everything in a file or library
# TODO: Import quadtree


def setup():
    global boids # TODO: add qt for quadtree
    colorMode(HSB, 360, 100, 100, 100)
    size(640, 360)   
    # size(640, 360)
    boids = []
    for i in range(100):
        boids.append(Boid(random(width), random(height)))
    
    # TODO: Initialize quadtree


def draw():
    global boids
    # TODO: Redefine quadtree
    
    # TODO: Insert points where all the boids are. Then, using personal data,
    # stuff the boid's identity inside the point. I'm not completely sure
    # why that works, so big TODO for that.
    
    background(220, 79, 35)
    gravity = PVector(0, 0.1)
    for boid in boids:
        # target = PVector(mouseX, mouseY)
        # TODO: query and pass that list inside. Also try making circles instead of
        # rectangles.
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
