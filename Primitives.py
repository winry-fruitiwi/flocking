# this has Point, Rectangle, and Particle classes.

# this describes an object that is literally just a point, but a more powerful point
# because it is active in a quadtree. Necessary for testing, but otherwise not so important.
class Point:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data # this holds the actual boid
    
    def show(self):
        stroke(0, 0, 100, 80)
        strokeWeight(3)
        point(self.x, self.y)


# this describes an object that is the boundary of a quadtree. Very important!
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w # width
        self.h = h # height
        
        # s = "I'm a rectangle at {},{} with width {} and height {}"
        # print s.format(x, y, w, h)
    
    def show(self):
        stroke(0, 0, 100, 80)
        strokeWeight(1)
        noFill()
        rectMode(CORNER)
        rect(self.x, self.y, self.w, self.h)
    
    
    # What happens when we intersect another rectangle? We get a jumbled mess, because
    # we need a function to sort everything out.
    def intersects(self, target):
        # target is another rectangle
        # there are eight cases where the target intersects the object, four where they
        # don't, so we choose the four knots.
        return not ((self.x + self.w < target.x) or 
                    (target.x + target.w < self.x) or 
                    (self.y + self.h < target.y) or 
                    (target.y + target.h < self.y))
    
    
    # used in Quadtree's insert, we check if the point is inside the coordinates
    def contains(self, p):
        # Is the point inside our boundaries? Well, that'll be tough, but I just need to
        # make sure the point is within the bounds.
        # We're using total inclusion
        
        return ((self.x <= p.x) and
                (p.x <= self.x + self.w) and 
                (self.y <= p.y) and 
                (p.y <= self.y + self.h))
        # return ((self.boundary.x <= p.x < (self.boundary.x + self.boundary.w)) and
        #         (self.boundary.y <= p.y < (self.boundary.y + self.boundary.h)))
