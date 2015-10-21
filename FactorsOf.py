import time
import Swarm
from Tkinter import *

class FactorsOf( Swarm.SwarmBase ):
    def __init__( self, *args, **kwargs ):
        super( FactorsOf, self).__init__( *args, **kwargs )

    def fitness( self, individual ):
        # print individual.solution
        # raw_input()
        ret = abs( reduce( lambda x,y: int(x) * int(y), individual.solution ) - 50 )
        print ret
        return ret

    def stop_condition( self ):
        fitnesses = map( self.fitness, self.swarm )
        print "Best fitness: ", min( fitnesses )
        return ( sum( fitnesses ) / len( fitnesses ) ) < 2

class Displayer( FactorsOf ):
    def __init__( self, *args, **kwargs ):
        super( Displayer, self ).__init__( *args, **kwargs )

        self.root = Tk()
        self.canvas = Canvas( self.root, width = 200, height = 200 )
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.after(1000, self.run, self.show )
        self.root.mainloop()

    def show( self, *args ):
        self.reset()
        for s in self.swarm:
            self.canvas.create_rectangle( s.solution[0] + 100, s.solution[1] + 100, s.solution[0] + 102, s.solution[1] + 102, fill = 'red' )
        self.canvas.update()

        time.sleep(0.25)

    def reset( self ):
        self.canvas.create_rectangle(0,0,200,200,fill="white") 

    

if __name__ == '__main__':
    disp = Displayer( 100, 2 )
