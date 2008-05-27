from abjad import *

### SIMPLE BEAD ###

def test_bead_navigation_01( ):
   '''NextBead works on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

def test_bead_navigation_02( ):
   '''NextBead works on simple Staff.'''
   t = Staff([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

#def test_bead_navigation_03( ):
#   '''NextBead works on simple Context.'''
#   t = Context([Note(i, (1,8)) for i in range(4)])
#   assert t[0]._navigator._nextBead is t[1]
#   assert t[1]._navigator._nextBead is t[2]
#   assert t[2]._navigator._nextBead is t[3]
#   assert t[3]._navigator._nextBead is None

def test_bead_navigation_04( ):
   '''NextBead works on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

def test_bead_navigation_05( ):
   '''NextBead works on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is None
   assert t[1]._navigator._nextBead is None
   assert t[2]._navigator._nextBead is None
   assert t[3]._navigator._nextBead is None

### LEVEL 1 NESTING ###

def test_bead_navigation_06( ):
   '''NextBead works on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s1[0]._navigator._nextBead is s1[1]
   assert s1[1]._navigator._nextBead is s1[2]
   assert s1[2]._navigator._nextBead is s1[3]
   assert s1[3]._navigator._nextBead is s2[0]

def test_bead_navigation_07( ):
   '''NextBead works on contiguous anonymous Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextBead is v1[1]
   assert v1[1]._navigator._nextBead is v1[2]
   assert v1[2]._navigator._nextBead is v1[3]
   assert v1[3]._navigator._nextBead is v2[0]

def test_bead_navigation_08( ):
   '''NextBead works on contiguous equally named Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'myvoice'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'myvoice'
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextBead is v1[1]
   assert v1[1]._navigator._nextBead is v1[2]
   assert v1[2]._navigator._nextBead is v1[3]
   assert v1[3]._navigator._nextBead is v2[0]

def test_bead_navigation_09( ):
   '''Beads do not connect through contiguous differently named Voices; 
      these are, by definition, two different "threads".'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'yourvoice'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'myvoice'
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextBead is v1[1]
   assert v1[1]._navigator._nextBead is v1[2]
   assert v1[2]._navigator._nextBead is v1[3]
   assert v1[3]._navigator._nextBead is None
   v2.invocation.name = None
   assert v1[3]._navigator._nextBead is None



### LEVEL 2 NESTING ###

def test_bead_navigation_20( ):
   '''Beads connect through simple symmetric depth 2 strutures. 
      Corresponding Voices and Staves are equally named.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'low'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'low'

   s1 = Staff([v1])
   s1.invocation.name = 'mystaff'
   s2 = Staff([v2])
   s2.invocation.name = 'mystaff'

   seq = Sequential([s1, s2])

   assert v1[3]._navigator._nextBead is v2[0]
   

def test_bead_navigation_21( ):
   '''Beads connect throght a symmetric depth 2 structure with parallel construct.'''
   v_low1 = Voice([Note(i, (1,8)) for i in range(4)])
   v_low1.invocation.name = 'low'
   v_low1.invocation.command = 'context'
   v_low2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v_low2.invocation.name = 'low'
   v_low2.invocation.command = 'context'
   v_high1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   v_high1.invocation.name = 'high'
   v_high1.invocation.command = 'context'
   v_high2 = Voice([Note(i, (1,8)) for i in range(16,20)])
   v_high2.invocation.name = 'high'
   v_high2.invocation.command = 'context'

   s1 = Staff([v_high1, v_low1])
   s1.invocation.name = 'mystaff'
   s1.invocation.command = 'context'
   s1.brackets = 'double-angle'
   s2 = Staff([v_low2, v_high2])
   s2.invocation.name = 'mystaff'
   s2.invocation.command = 'context'
   s2.brackets = 'double-angle'

   seq = Sequential([s1, s2])

   assert v_low1[3]._navigator._nextBead is v_low2[0]
   assert v_high1[3]._navigator._nextBead is v_high2[0]
      
def test_bead_navigation_22( ):
   '''Beads connect through a symmetrical depth 2 structure 
      with a parallel Staff and a sequential Staff constructs.'''
   v_low1 = Voice([Note(i, (1,8)) for i in range(4)])
   v_low1.invocation.name = 'low'
   v_low2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v_low2.invocation.name = 'low'
   v_high = Voice([Note(i, (1,8)) for i in range(12,16)])
   v_high.invocation.name = 'high'

   s1 = Staff([v_high, v_low1])
   s1.invocation.name = 'mystaff'
   s1.brackets = 'double-angle'
   s2 = Staff([v_low2])
   s2.invocation.name = 'mystaff'

   seq = Sequential([s1, s2])

   assert v_low1[3]._navigator._nextBead is v_low2[0]


### DEPTH ASYMMETRICAL STRUCTURES ###
### Parentage asymmetrical structures work IF tautological ###

def test_bead_navigation_30( ):
   '''NextBead works on symmetrical nested Sequentials in a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])
   assert s1[0][0]._navigator._nextBead is s1[0][1]
   assert s1[0][1]._navigator._nextBead is s1[0][2]
   assert s1[0][2]._navigator._nextBead is s1[0][3]
   assert s1[0][3]._navigator._nextBead is s2[0][0]

def test_bead_navigation_31( ):
   '''Tautological parentage asymmetries result in symmetric (balanced) 
      threaded parentage.  These work well.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   s2 = Sequential([s2])
   s2 = Sequential([s2])
   t = Voice([s1, s2])
   assert s1[0]._navigator._nextBead is s1[1]
   assert s1[1]._navigator._nextBead is s1[2]
   assert s1[2]._navigator._nextBead is s1[3]
   assert s1[3]._navigator._nextBead is s2[0][0][0]

def test_bead_navigation_32( ):
   '''Tautological parentage asymmetries result in symmetric (balanced) 
      threaded parentage.  These work well.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s1 = Sequential([s1])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s1[0][0][0]._navigator._nextBead is s1[0][0][1]
   assert s1[0][0][1]._navigator._nextBead is s1[0][0][2]
   assert s1[0][0][2]._navigator._nextBead is s1[0][0][3]
   assert s1[0][0][3]._navigator._nextBead is s2[0]

### Parentage asymmetrical structures DON'T work if NOT tautological ###

def test_bead_navigation_33( ):
   '''NextBead returns None in asymmetric thread parentage structurese.'''
   v1 = Voice([Note(i , (1,8)) for i in range(3)])
   n = Note(3, (1,8))
   v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
   t = Staff([v1, n, v2])
   assert v1[-1]._navigator._nextBead is None
   assert n._navigator._nextBead is None


### NON-CONTIGUOUS / BROKEN THREADS ###

def test_bead_navigation_40( ):
   '''Non-contiguous / broken threads do not connect.'''
   ###
   ### do we want them to connect? probably not...
   ###
   v1 = Voice([Note(i , (1,8)) for i in range(3)])
   v1.invocation.name = 'myvoice'
   v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
   v2.invocation.name = 'yourvoice'
   v3 = Voice([Note(i , (1,8)) for i in range(4,8)])
   v3.invocation.name = 'myvoice'
   t = Staff([v1, v2, v3])

   assert v1[-1]._navigator._nextBead is None
   assert v2[-1]._navigator._nextBead is None

   v2.invocation.name = None
   assert v1[-1]._navigator._nextBead is None
   assert v2[-1]._navigator._nextBead is None


### TAUTOLOGICAL NESTING ###

def test_bead_navigation_50a( ):
   '''NextBead works on nested anonymous Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(3)])
   vout = Voice([vin, Note(3, (1,8))])
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vin[2]._navigator._nextBead is vout[1]

def test_bead_navigation_50b( ):
   '''NextBead works on nested anonymous Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(1,4)])
   vout = Voice([Note(0, (1,8)), vin])
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vout[0]._navigator._nextBead is vin[0]

def test_bead_navigation_51a( ):
   '''NextBead works on nested equally named Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(3)])
   vin.invocation.name = 'myvoice'
   vout = Voice([vin, Note(3, (1,8))])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vin[2]._navigator._nextBead is vout[1]

def test_bead_navigation_51b( ):
   '''NextBead works on nested equally named Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(1,4)])
   vin.invocation.name = 'myvoice'
   vout = Voice([Note(0, (1,8)), vin])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vout[0]._navigator._nextBead is vin[0]

def test_bead_navigation_52a( ):
   '''NextBead return None on nested *differently* named Voices.
      This is what we want because these are NOT tautologies.''' 
   vin = Voice([Note(i, (1,8)) for i in range(3)])
   vin.invocation.name = 'yourvoice'
   vout = Voice([vin, Note(3, (1,8))])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vin[2]._navigator._nextBead is None

def test_bead_navigation_52b( ):
   '''NextBead return None on nested *differently* named Voices.
      This is what we want because these are NOT tautologies.''' 
   vin = Voice([Note(i, (1,8)) for i in range(1, 4)])
   vin.invocation.name = 'yourvoice'
   vout = Voice([Note(0, (1,8)), vin])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vout[0]._navigator._nextBead is None

