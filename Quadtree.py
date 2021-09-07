

from Primitives import *
# quadtree is the goal. It should have a boundary, and split up if it hasn't divided. Later
# I won't display the points so I can see the quadtree's miracle!
class Quadtree:
    def __init__(self, boundary, capacity):
        # see Rectangle's comment
        self.boundary = boundary
        # if this quadtree has divided, it should not divide again because its capacity is full
        self.divided = False
        # if we don't declare the four instance variables, we'll never be able to!
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
        # what's the point of a quadtree without a capacity? Wasted frames?
        self.capacity = capacity
        # just holds the points that a quadtree has
        self.points = []
    
    
    # we can insert a point. If the capacity is full, we divide (in the function after this)
    def insert(self, p):
        if not self.boundary.contains(p):
            return False # we don't want points that aren't in the quadtree!
        
        
        if len(self.points) < self.capacity:
            self.points.append(p)
            return True
        
        # if we're full, we need to subdivide!
        else:
            # call subdivide, and whoever has the point gets it. However, the first guy
            # called on will be favored.
            if not self.divided:
                self.subdivide()
            if self.northwest.insert(p):
                return True
            
            if self.northeast.insert(p):
                return True
            
            if self.southwest.insert(p):
                return True
            
            if self.southeast.insert(p):
                return True
    
    
    # we want to find how many points are in a specified boundary. How? With a query!
    def query(self, target):
        # represents what points we've grouped up. We can use our mouse as a pointfinder!
        found = []
        # if there's nothing around, forget looking anywhere, we won't find what we need.
        if not self.boundary.intersects(target):
            pass
        
        else:
            for p in self.points:
                if target.contains(p):
                    found.append(p)
            
            if self.divided:
                found += self.northwest.query(target)
                found += self.northeast.query(target)
                found += self.southwest.query(target)
                found += self.southeast.query(target)
        
        return found
    
    
    # used in insert, we divide this quadtree into four quadrants: nw, ne, sw, se.
    def subdivide(self):
        # I like to initiate things in order!
        
        # we start with nw, which has all the same coordinates. It's a warmup, as I say.
        nw = Rectangle(self.boundary.x,
                       self.boundary.y,
                       self.boundary.w/2.0,
                       self.boundary.h/2.0)
        self.northwest = Quadtree(nw, self.capacity)
        
        # now for northeast...
        ne = Rectangle(self.boundary.x + self.boundary.w/2.0, # x
                       self.boundary.y, # y
                       self.boundary.w/2.0, # w
                       self.boundary.h/2.0) # h
        self.northeast = Quadtree(ne, self.capacity)
        
        # southwest...
        sw = Rectangle(self.boundary.x,
                       self.boundary.y + self.boundary.h/2.0,
                       self.boundary.w/2.0,
                       self.boundary.h/2.0)
        self.southwest = Quadtree(sw, self.capacity)
        
        # and finally the boss, southwest.
        se = Rectangle(self.boundary.x + self.boundary.w/2.0,
                       self.boundary.y + self.boundary.h/2.0,
                       self.boundary.w/2.0,
                       self.boundary.h/2.0)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True
    
    
    # how are we supposed to see a quadtree in action without a show method?
    def show(self):
        # if we've divided before, we have children. So we first draw our own rectangle,
        # then recursively tell our children to call their own version of show.
        # pushMatrix()
        # translate(self.x, self.y)
        # stroke(0, 0, 100, 80)
        # self.boundary.show()
        # popMatrix() # we don't need any of this! It's just trash!
        self.boundary.show()
        if self.divided:
            self.northeast.show()
            self.northwest.show()
            self.southeast.show()
            self.southwest.show()
