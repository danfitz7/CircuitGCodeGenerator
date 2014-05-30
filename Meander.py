from mecode import G
from math import sqrt

g = G(
    print_lines=False,
    outfile=r"C:\Users\lewislab\Desktop\DOGBONEcircuit-path.gcode",
    aerotech_include=False,
)

#Extra G Codes
PRESSURE_ON = 'M400 \nM42 P32 S255'
PRESSURE_OFF = 'M400 \nM42 P32 S0'
PAUSE="M0\nM1\nM25\nM226"     

class Point(object):
    """Point class with public x and y attributes """
 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
 
    def dist(self, p):
        """return the Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        return sqrt(dx*dx + dy*dy)
 
    def reset(self):
        self.x = 0
        self.y = 0

    def __add__(self, p):
        """return a new point found by adding self and p. This method is
        called by e.g. p+q for points p and q"""
        return Point(self.x+p.x, self.y+p.y)
 
    def __repr__(self):
        """return a string representation of this point. This method is
        called by the repr() function, and
        also the str() function. It should produce a string that, when
        evaluated, returns a point with the 
        same data."""
        return 'Point(%d,%d)' % (self.x, self.y)   

class CircuitPoint(Point):
    def startTrace(g,offset):
        pass
        
    def endTrace(g,offset):
        pass  
            
class Pad(Point):
    padFillingZOffzet = -0.3            #height of the nozzle relative whle filling pads relative to their top

    startTrace(g,offset):
        p=offset+self
        g.abs_move(p.x,p.y,padFilingOffset)
        
    endTrace(g,offset):
        p=offset+self
        g.abs_move(p.x,p.y,padFilingOffset)

class Trace:
    """Trace class contains a list of points that define a single (non-branching) trace"""
    def __init__(self, points = []):
        self._points = points
        
class Circuit:
    def __init__(self, traces = [], top = 5.39):
        self._traces = traces
        self._top = top

def print_circuit(top, feed, fast_feed, dwell, pressure, axis, valve, valve_bank = True, y_negative = False):
    
   
    #circuit printing height behavior
    travelHeightOffset = 2               #Z height relative to "top"to travel safely at
    dabZOffset = -0.4                  #height of the nozzle relative to the top of the channels for "dapping" the trace at their ends (avoid stringing)
    contactPadFillingZOffset = -0.7
    
    #timing bahavior
    dabDwellTime=5000  #in ms
    dwellTimeMultiplier=1000   

    #DirectWrite behavior
    extrusionRetractionDist=10
    
#Circuit Trace Corner Positions
C1 = Point(-12.94,-37.407)
C2 = Point(-12.94,-11.407)
C3 = Point(-2.24,-11.407)
C4 = Point(-2.24,53.163)
C5 = Point(2.76,53.163)
C6 = Point(13.76,-3.15)
C7 = Point(13.76,-37.407)
C8 = Point(10.76,-11.407)
C9 = Point(10.76, -27.407)

#Ink Transitions
T1 = Point(-2.24,-3.15)
T2 = Point(-2.76,-3.15)

#Resistor contacts
R1 = Point(-10.74,-11.407)
R2 = Point(-7.14,-11.407)

#Pins
P_Gnd = Point(-10.74, -37.407)
P_A0  = Point(8.01,-27.407)
P_Vcc = Point(8.01,037.407)

#Signal Traces
Gnd_R = Trace([P_Gnd,C1,C2,R1])
R_T1  = Trace([R2,C3,T1])
T1_T2 = Trace([T1,C4,C5,T2])
C3_A0 = Trace([C3,C6,C9,P_A0])
T2_Vcc =Trace([T2,C6,C7,P_Vcc])

#make our torqueWrench
torqueWrenchCircuit = Circuit(traces = [Gnd_R, R_T1, C3_A0, T2_Vcc, T1_T2], top = 5.39)
print_circuit(torqueWrenchCircuit) 
 

