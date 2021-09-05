# this creates an object that flocks with others. Without quadtrees, the
# runtime of each algorithm is O(N^2) so we can use them later.


class Boid(object): # if we want to inherit
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D() # identical to PVector(0, 0) and PVector(0, 0, 0)
        self.acc = PVector()
        self.max_speed = 4 # to prevent things from getting too fast
        # keeps things from turning around faster than they can run!
        self.max_force = 0.2
    
    
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
        pushMatrix()
        noStroke()
        translate(self.pos.x, self.pos.y)
        rotate(self.vel.heading())
        fill(0, 0, 100, 80)
        ellipse(0, 0, 16, 4)
        triangle(0, 0,
                 -14, 4,
                 -14, -4)
        noFill()
        popMatrix()

    
    # this creates a correction force that returns a force  vector at the end
    def seek(self, target): # target is a PVector
        steering_force = PVector.sub(target, self.pos)
        steering_force.setMag(self.max_speed)
        # steering_force = desired_velocity - current_velocity
        
        # we want to get to the target as fast as possible, but we're heading
        # the wrong way. To correct this, we want a steering with the opposite
        # angle relative to the target so that we can go in a relatively
        # straight line.
        steering_force.sub(self.vel)
        steering_force.limit(self.max_force)
        return steering_force
    
    
    # this is very similar to the seek found in other Autonomous Characters
    # papers from Craig Reynolds, except we don't have that position subtract!
    # The second argument is the result of the first line in the
    def velocity_seek(self, desired_velocity): # desired_velocity is a PVector
        # normally we'd have the error correction step, but we don't need that anymore
        # because we're already including it in desired_velocity!
        # steering_force = desired_velocity - current_velocity
        steering_force = desired_velocity.setMag(self.max_speed)
        
        # we want to get to the target as fast as possible, but we're heading
        # the wrong way. To correct this, we want a steering with the opposite
        # angle relative to the target so that we can go in a relatively
        # straight line.
        steering_force.sub(self.vel)
        steering_force.limit(self.max_force)
        return steering_force
    
    
    # makes the velocity equal to the average velocity of each boid
    def deprecated_align(self, boids):
        # we want 3 variables to describe what our function will do...
        perception_radius = 40 # you do not want a flock with a million boids.
        average = PVector() # we just want to start with an empty slate!
        total = 0 # keep track of how many boids we have
        # noFill()
        # stroke(0, 0, 100, 80)
        # circle(self.pos.x, self.pos.y, perception_radius*2)

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
            steering_force = average.div(total)

        else:
            return PVector(0, 0)

        # desired_velocity = self.vel - target.vel
        
        steering_force.setMag(self.max_speed)
        steering_force.sub(self.vel)
        steering_force.limit(self.max_force)
        return steering_force


    # makes the boid go close to the average position
    def deprecated_cohere(self, boids):
        # we want 3 variables to describe what our function will do...
        perception_radius = 40 # you do not want a flock with a million boids.
        average = PVector() # we just want to start with an empty slate!
        total = 0 # keep track of how many boids we have
        # noFill()
        # stroke(0, 0, 100, 80)
        # circle(self.pos.x, self.pos.y, perception_radius*2)
        # now loop through every boid...
        for boid in boids:
            # now check if they're within a certain perception radius. If distance = 0,
            # we're either in a rare case where the boid is right on us or it's just us.
            distance = dist(self.pos.x, self.pos.y, boid.pos.x, boid.pos.y)
            if distance < perception_radius and distance > 0:
                # if they are, add to the average and then divide it later.
                average.add(boid.pos)
                total += 1

        if total > 0:
            average.div(total)

        else:
            return PVector(0, 0)

        # desired_velocity = self.vel - target.vel
        steering_force = PVector.sub(average, self.pos)
        steering_force.setMag(self.max_speed)
        steering_force.sub(self.vel)
        steering_force.limit(self.max_force)
        return steering_force


    # keeps the boid from crashing into another flockmate, especially to
    # keep anyone from cracking each other's skulls.
    def deprecated_separate(self, boids):
        # we want 3 variables to describe what our function will do...
        perception_radius = 30 # you do not want a flock with a million boids.
        average = PVector() # we just want to start with an empty slate!
        total = 0 # keep track of how many boids we have
        # noFill()
        # stroke(0, 0, 100, 80)
        # circle(self.pos.x, self.pos.y, perception_radius*2)
        # now loop through every boid...
        for boid in boids:
            # now check if they're within a certain perception radius. If distance = 0,
            # we're either in a rare case where the boid is right on us or it's just us.
            distance = dist(self.pos.x, self.pos.y, boid.pos.x, boid.pos.y)
            if distance < perception_radius and distance > 0:
                # if they are, add to the average and then divide it later.
                difference = PVector.sub(self.pos, boid.pos)
                difference.div(distance)
                average.add(difference)
                total += 1

        if total > 0:
            steering_force = average.div(total)

        else:
            return PVector(0, 0)

        # desired_velocity = self.vel - target.vel
        steering_force.setMag(self.max_speed)
        steering_force.sub(self.vel)
        steering_force.limit(self.max_force)
        return steering_force.mult(1.5)
    
    
    # makes each boid match velocities with local flockmates
    def align(self, boids):
        # without the word "local" we'd be matching forever!
        perception_radius = 40
        # to keep track of the average
        average = PVector()
        # how many boids did we visit?
        total = 0
        
        for boid in boids:
            distance = PVector.dist(self.pos, boid.pos)
            if distance <= perception_radius and boid != self:
                total += 1 # divide the average by this later
                average.add(boid.vel)
        
        # after all that is done, we call seek_velocity!
        if total > 0:
            steering_force = average.div(total)
            return self.velocity_seek(steering_force)
        else:
            return PVector()
    
    
    # makes everyone call their flocking functions.
    def flock(self, boids):
        # aligns the flock
        alignment = self.align(boids).mult(1)
        self.apply_force(alignment)
        
        # # makes the flock cohere
        # coherence = self.cohere(boids).mult(1)
        # self.apply_force(coherence)
        
        # separation = self.separate(boids).mult(1)
        # self.apply_force(separation)


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
