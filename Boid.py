# this creates an object that flocks with others. Without quadtrees, the
# runtime of each algorithm is O(N^2) so we can use them later.


class Boid(object): # if we want to inherit
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D() # identical to PVector(0, 0) and PVector(0, 0, 0)
        self.acc = PVector()
        self.max_speed = 4 # to prevent things from getting too fast
        # keeps things from turning around faster than they can run!
        self.max_force = 0.1
    
    
    # updates all the boid's values
    def update(self):
        self.pos.add(self.vel)
        self.vel.add(self.acc).limit(self.max_speed)
        self.acc = PVector()


    # applies a force to the boid. Daniel didn't do this, but let's just make
    # things more intuitive.
    def apply_force(self, force):
        # F = ma > a = F/m. If mass is one, which we're assuming is true, a = f.
        self.acc.add(force)


    # shows the object as a circle. Later, we can get more complex with either a hackbot
    # or a very simple triangle.
    def show(self):
        noStroke()
        fill(0, 0, 100, 80)
        circle(self.pos.x, self.pos.y, 8)


    # makes the velocity equal to the average velocity of each boid
    def align(self, boids):
        # we want 3 variables to describe what our function will do...
        perception_radius = 20 # you do not want a flock with a million boids.
        average = PVector() # we just want to start with an empty slate!
        total = 0 # keep track of how many boids we have

        # now loop through every boid...
        for boid in boids:
            # now check if they're within a certain perception radius. If distance = 0,
            # we're either in a rare case where the boid is right on us or it's just us.
            distance = dist(self.pos.x, self.pos.y, boid.pos.x, boid.pos.y)
            if distance < perception_radius and distance > 0:
                # if they are, add to the average and then divide it later.
                average.add(boid.vel)
                total += 1

        if total > 0:
            average.div(total)

        else:
            return PVector(0, 0)

        # desired_velocity = self.vel - target.vel
        steering_force = PVector.sub(average, self.vel)
        steering_force.setMag(self.max_force)
        return steering_force


    # makes everyone call their flocking functions.
    def flock(self, boids):
        alignment = self.align(boids)
        self.apply_force(alignment)


    # makes the boid go close to the average position
    def cohere(self, boids):
        pass


    # keeps the boid from crashing into another flockmate, especially to
    # keep anyone from cracking each other's skulls.
    def separate(self, boids):
        pass


    # want to kiss goodbye to a flock forever? No! You want to keep them around!
    def edges(self):
        # right edge
        if self.pos.x >= width:
            self.pos.x = 0

        # left edge
        elif self.pos.x <= 0:
            self.pos.x = width

        # top edge
        elif self.pos.y <= 0:
            self.pos.y = height

        # bottom edge
        elif self.pos.y >= height:
            self.pos.y = 0