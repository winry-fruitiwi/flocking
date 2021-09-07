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

    
    # makes everyone call their flocking functions.
    def flock(self, boids): # deprecated for now.
        # aligns the flock
        alignment = self.align(boids).mult(1)
        self.apply_force(alignment)
        
        # makes the flock cohere
        coherence = self.cohere(boids).mult(1)
        self.apply_force(coherence)
        
        # keeps the flock separated and gives them breathing space
        separation = self.separate(boids).mult(2)
        self.apply_force(separation)
    
    
    # the boid is looking for something but is going in the wrong direction.
    # It needs a correction force to steer itself to the right place!
    # Uses Craig Reynold's equation for steering behaviours,
    # steering_force = desired_velocity - current_velocity
    def seek(self, location): # target is a PVector location.
        # The only difference between velocity_seek and normal seek is that
        # we start with just a location, so we need a vector from our location
        # to the argument. Then we simply call velocity_seek on it, and we're done!
        velocity = PVector.sub(location, self.pos)
        return self.velocity_seek(velocity)
    
    
    # For this variation of seek, we don't care about positions.
    # We just want a velocity, so throw that first statement of plain seek into the 
    # trash can and finish the rest of the function!
    def velocity_seek(self, velocity): # velocity is also a PVector velocity
        # we omit the first line from seek and then everything else proceeds as usual.
        # Now we want to move at our maximum velocity so we set the vector's
        # magnitude to our max speed.
        velocity.setMag(self.max_speed)
        
        # now, we use Craig Reynold's equation using the old velocity minus ours.
        velocity = PVector.sub(velocity, self.vel)
        
        # Finally, we can turn this into what we interpret as a force vector
        # by limiting this to the maximum force. Note that Python doesn't care about
        # the type of PVector, it just cares that the object is a PVector.
        velocity.setMag(self.max_force)
        # We've finished all that hard work, and it's almost time to celebrate.
        # One more statement 'till we can: return the fruit of our labour!
        return velocity
    
    
    # A duck-boid looks around and he wants to move the same direction as his local friends.
    # This function handles all that and now the duck is satisfied!
    def align(self, boids): # boids is a list filled with the duck's friends.
        # the word "local" is very important in this format. Without that word,
        # the system would no longer be natural because everyone would move in 
        # the same direction. This means we need a perception radius!
        perception_radius = 50
        # the duck wants to move in the same direction as his local friends, so
        # needs to move in their average direction.
        average = PVector()
        # we need to keep track of how many boids there are, or else our average
        # would be more like total_velocity instead of average_velocity.
        total = 0
        
        # now we loop through all the boids in the boids list
        for boid in boids:
            distance = PVector.dist(self.pos, boid.pos)
            # if the boid is within the perception radius, we add its velocity
            # to the average variable, then increment the total variable
            if distance <= perception_radius and boid != self:
                total += 1
                average.add(boid.vel)
        
        if total > 0:
            # we divide by the total to get the average heading. Since we have a velocity,
            # we call seek_velocity and return that.
            average.div(total)
            return self.velocity_seek(average)
        
        else:
            return PVector(0, 0) # this means we didn't find anything
    
    
    # A penguin-boid needs to stay warm, and the best place for that is the middle
    # of all the penguins. This function handles that.
    def cohere(self, boids): # boids is a list of all the boid objects
        pass
        # we define the same variables as in align, except the average velocity
        # is now an average position.
        perception_radius = 50
        average = PVector()
        total = 0
        # we do the same as in align
        for boid in boids:
            distance = PVector.dist(self.pos, boid.pos)
            # we make the same check but add the position of the boid instead of
            # its velocity.
            if distance <= perception_radius and boid != self:
                total += 1
                average.add(boid.pos)
        
        # after dividing the average by the total we have a position so we call seek.
        if total > 0:
            average.div(total)
            return self.seek(average) # because we have a position!
        
        else:
            return PVector()
        
    
    # A porcupine-boid has a lot of spines and doesn't want to injure his friends,
    # so he gets away from them if they come too close.
    def separate(self, boids):
        # all the same variables as in align!
        perception_radius = 30
        average = PVector()
        total = 0
        
        # now loop again
        for boid in boids:
            # we make the same check but there's a trick now! We need a vector from
            # the other porcupine to us:
            #    boid.pos - self.pos            
            # then divide that by the distance
            # this should be inversely proportional to the distance
            # boids closer by exert greater repulsive force.
            # We add that to the average.
            distance = PVector.dist(self.pos, boid.pos) # order does not matter for distance
            if distance <= perception_radius and boid != self:
                diff = PVector.sub(self.pos, boid.pos)
                diff.div(distance)
                average.add(diff)
                total += 1
        
        # The tricky part is over. Now, we proceed as we did in align.
        if total > 0:
            average.div(total)
            return self.velocity_seek(average)
        
        else:
            return PVector(0, 0)
    

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
