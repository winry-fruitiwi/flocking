# this creates an object that flocks with others. Without quadtrees, the
# runtime of each algorithm is O(N^2) so we can use them later.


class Boid(object): # if we want to inherit
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector() # identical to PVector(0, 0) and PVector(0, 0, 0)
        self.acc = PVector()
    
    
    # updates all the boid's values
    def update(self):
        pass
    
    
    # applies a force to the boid. Daniel didn't do this, but let's just make
    # things more intuitive.
    def apply_force(self):
        pass
    
    
    # makes the velocity equal to the average velocity of each boid
    def align(self, boids):
        pass
    
    
    # makes the boid go close to the average position
    def cohere(self, boids):
        pass
    
    
    # keeps the boid from crashing into another flockmate.
    def separate(self, boids):
        pass
