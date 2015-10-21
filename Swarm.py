# Fitness function
# Stop condition
# Update

import random

class Solution( object ):
    class SolutionError( Exception ):
        def __init__( self, value ):
            self.value = value

        def __repr__( self ):
            return "SolutionException: " + self.value

    def __init__( self, initial_value ):
        self.value = initial_value

    def __add__( self, other ):
        return Solution( map( lambda x: x[0] + x[1], zip( self.value, other.value )))
        
    def __sub__( self, other ):
        return Solution( map( lambda x: x[0] - x[1], zip( self.value, other.value )))

    def __mul__( self, multiplier ):
        if hasattr( multiplier, '__len__' ):
            try:
                return Solution( map( lambda x: x[0] * x[1], zip( self.value, multiplier.value )))
            except Exception as e:
                print e.message
                raise self.SolutionError( "Only solutions of the same length may be multiplied against one another." )
        else:
            return Solution( map( lambda x: x * multiplier, self.value ))

    def __div__( self, divisor ):
        if hasattr( divisor, '__len__' ):
            try:
                return Solution( map( lambda x: (x[0] / x[1]) if (x[0] != 0 and x[1] != 0) else 0, zip( self.value, divisor.value )))
            except Exception as e:
                print e.message
                raise self.SolutionError( "Only solutions of the same length may be multiplied against one another." )
        else:
            if divisor != 0:
                return Solution( map( lambda x: x / divisor, self.value ))
            else:
                return Solution( [ 0 for x in range( len( self.value ) ) ] )
                
    def __rdiv__( self, divisor ):
        if hasattr( divisor, '__len__' ):
            try:
                return Solution( map( lambda x: x[1] / x[0], zip( self.value, divisor.value )))
            except Exception as e:
                print e.message
                raise self.SolutionError( "Only solutions of the same length may be multiplied against one another." )
        else:
            if divisor != 0:
                return Solution( map( lambda x: (divisor / x) if x != 0 else 0, self.value ))
            else:
                return Solution( [ 0  for x in range( len( self.value ) ) ] )

    def __getitem__( self, index ):
        return self.value[ index ]
        
    def __setitem__( self, index, val ):
        self.value[ index ] = val

    def __len__( self ):
        return len( self.value )

    def __repr__( self ):
        return str( self.value )
        

    
class Individual( object ):
    def __init__( self, initial, velocity, influence_magnitude = 0.01, velocity_cap = 5 ):
        if len( initial ) != len( velocity ):
            raise Exception( "Dimensions of position and velocity should match" )

        self.solution            = Solution( initial )
        self.velocity            = Solution( velocity )
        self.influence_magnitude = influence_magnitude
        self.velocity_cap        = 10

    def cap_velocity( self ):
        if self.velocity.value[0] > self.velocity_cap:
            self.velocity.value[0] = self.velocity_cap
        elif self.velocity.value[0] < -self.velocity_cap:
            self.velocity.value[0] = - self.velocity_cap

        if self.velocity.value[1] > self.velocity_cap:
            self.velocity.value[1] = self.velocity_cap
        elif self.velocity.value[1] < -self.velocity_cap:
            self.velocity.value[1] = - self.velocity_cap
            
    def update( self, best ):
        # print "Before: ", self.solution
        # print "Velocity: ", self.velocity
        # print "Best: ", best.solution
        self.velocity *= 0.9 # Drag
        change = (best.solution - self.solution) / 7
        self.velocity += change # * self.influence_magnitude
        # self.cap_velocity()
        # self.velocity = Solution( map( lambda i: int(i), self.velocity ) )
        self.solution += self.velocity
        # print "After: ", self.solution
        
class SwarmBase( object ):
    def __init__( self, amt, dimension ):
        self.swarm = []
        for i in range( amt ):
            self.swarm.append( Individual( [ random.randint( -99, 99 ) for x in range( dimension ) ],
                                           [ random.randint( -2, 2 ) for y in range( dimension ) ] ) )

    def fitness( self ):
        raise NotImplementedError

    def best( self, minimise = True ):
        f = lambda x,y: x if self.fitness(x) > self.fitness(y) else y

        if minimise:
            f = lambda x,y: x if self.fitness(x) < self.fitness(y) else y
    
        return reduce( f, self.swarm )

    def advance( self ):
        best = self.best()

        for s in self.swarm:
            s.update( best )

    def stop_condition( self ):
        raise NotImplementedError
        
    def run( self, extra_func = None ):
        while not self.stop_condition():
            self.advance()
            if extra_func != None:
                extra_func( self.swarm )

        print "Cooked!"
        print self.best().solution
