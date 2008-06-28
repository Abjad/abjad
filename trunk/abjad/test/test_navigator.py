from abjad import *

### SIMPLE BEAD ###

def test_bead_navigation_01( ):
   '''nextBead and prevBead work on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

   assert t[0]._navigator._prevBead is None
   assert t[1]._navigator._prevBead is t[0]
   assert t[2]._navigator._prevBead is t[1]
   assert t[3]._navigator._prevBead is t[2]


def test_bead_navigation_02( ):
   '''NextBead and prevBead work on simple Staff.'''
   t = Staff([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

   assert t[0]._navigator._prevBead is None
   assert t[1]._navigator._prevBead is t[0]
   assert t[2]._navigator._prevBead is t[1]
   assert t[3]._navigator._prevBead is t[2]


#def test_bead_navigation_03( ):
#   '''nextBead and prevBead work on simple Context.'''
#   t = Context([Note(i, (1,8)) for i in range(4)])
#   assert t[0]._navigator._nextBead is t[1]
#   assert t[1]._navigator._nextBead is t[2]
#   assert t[2]._navigator._nextBead is t[3]
#   assert t[3]._navigator._nextBead is None

def test_bead_navigation_04( ):
   '''NextBead and prevBead work on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is t[1]
   assert t[1]._navigator._nextBead is t[2]
   assert t[2]._navigator._nextBead is t[3]
   assert t[3]._navigator._nextBead is None

   assert t[0]._navigator._prevBead is None
   assert t[1]._navigator._prevBead is t[0]
   assert t[2]._navigator._prevBead is t[1]
   assert t[3]._navigator._prevBead is t[2]


def test_bead_navigation_05( ):
   '''NextBead and prevBead work on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextBead is None
   assert t[1]._navigator._nextBead is None
   assert t[2]._navigator._nextBead is None
   assert t[3]._navigator._nextBead is None

   assert t[0]._navigator._prevBead is None
   assert t[1]._navigator._prevBead is None
   assert t[2]._navigator._prevBead is None
   assert t[3]._navigator._prevBead is None

### LEVEL 1 NESTING ###

def test_bead_navigation_06( ):
   '''NextBead and prevBead work on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s1[0]._navigator._nextBead is s1[1]
   assert s1[1]._navigator._nextBead is s1[2]
   assert s1[2]._navigator._nextBead is s1[3]
   assert s1[3]._navigator._nextBead is s2[0]

   assert s1[1]._navigator._prevBead is s1[0]
   assert s1[2]._navigator._prevBead is s1[1]
   assert s1[3]._navigator._prevBead is s1[2]
   assert s2[0]._navigator._prevBead is s1[3]

def test_bead_navigation_07( ):
   '''NextBead and prevBead work on contiguous anonymous Voices 
   inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextBead is v1[1]
   assert v1[1]._navigator._nextBead is v1[2]
   assert v1[2]._navigator._nextBead is v1[3]
   assert v1[3]._navigator._nextBead is v2[0]

   assert v1[1]._navigator._prevBead is v1[0]
   assert v1[2]._navigator._prevBead is v1[1]
   assert v1[3]._navigator._prevBead is v1[2]
   assert v2[0]._navigator._prevBead is v1[3]

def test_bead_navigation_08( ):
   '''NextBead and prevBead work on contiguous equally named Voices 
   inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'myvoice'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'myvoice'
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextBead is v1[1]
   assert v1[1]._navigator._nextBead is v1[2]
   assert v1[2]._navigator._nextBead is v1[3]
   assert v1[3]._navigator._nextBead is v2[0]

   assert v1[1]._navigator._prevBead is v1[0]
   assert v1[2]._navigator._prevBead is v1[1]
   assert v1[3]._navigator._prevBead is v1[2]
   assert v2[0]._navigator._prevBead is v1[3]

def test_bead_navigation_09( ):
   '''Beads do not connect through contiguous unequally named Voices; 
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

   assert v2[1]._navigator._prevBead is v2[0]
   assert v2[2]._navigator._prevBead is v2[1]
   assert v2[3]._navigator._prevBead is v2[2]
   assert v2[0]._navigator._prevBead is None


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
   assert v2[0]._navigator._prevBead is v1[3]
   

def test_bead_navigation_21( ):
   '''Beads connect throght a symmetric depth 2 structure with parallel construct.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl1.invocation.command = 'context'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vl2.invocation.command = 'context'
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh1.invocation.name = 'high'
   vh1.invocation.command = 'context'
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])
   vh2.invocation.name = 'high'
   vh2.invocation.command = 'context'

   s1 = Staff([vh1, vl1])
   s1.invocation.name = 'mystaff'
   s1.invocation.command = 'context'
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.invocation.name = 'mystaff'
   s2.invocation.command = 'context'
   s2.brackets = 'double-angle'

   seq = Sequential([s1, s2])

   assert vl1[3]._navigator._nextBead is vl2[0]
   assert vh1[3]._navigator._nextBead is vh2[0]

   assert vl2[0]._navigator._prevBead is vl1[3]
   assert vh2[0]._navigator._prevBead is vh1[3]
      

def test_bead_navigation_22( ):
   '''Beads connect through a symmetrical depth 2 structure 
      with a parallel Staff and a sequential Staff constructs.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vh = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh.invocation.name = 'high'

   s1 = Staff([vh, vl1])
   s1.invocation.name = 'mystaff'
   s1.brackets = 'double-angle'
   s2 = Staff([vl2])
   s2.invocation.name = 'mystaff'

   seq = Sequential([s1, s2])

   assert vl1[3]._navigator._nextBead is vl2[0]
   assert vl2[0]._navigator._prevBead is vl1[3]


### DEPTH ASYMMETRICAL STRUCTURES ###
### Parentage asymmetrical structures work IF tautological ###

def test_bead_navigation_30( ):
   '''nextBead and prevBead work on symmetrical nested Sequentials in a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])
   assert s1[0][0]._navigator._nextBead is s1[0][1]
   assert s1[0][1]._navigator._nextBead is s1[0][2]
   assert s1[0][2]._navigator._nextBead is s1[0][3]
   assert s1[0][3]._navigator._nextBead is s2[0][0]

   assert s2[0][1]._navigator._prevBead is s2[0][0]
   assert s2[0][2]._navigator._prevBead is s2[0][1]
   assert s2[0][3]._navigator._prevBead is s2[0][2]
   assert s2[0][0]._navigator._prevBead is s1[0][3]


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

   assert s2[0][0][1]._navigator._prevBead is s2[0][0][0]
   assert s2[0][0][2]._navigator._prevBead is s2[0][0][1]
   assert s2[0][0][3]._navigator._prevBead is s2[0][0][2]
   assert s2[0][0][0]._navigator._prevBead is s1[3]


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

   assert s2[0]._navigator._prevBead is s1[0][0][3]
   assert s2[1]._navigator._prevBead is s2[0]
   assert s2[2]._navigator._prevBead is s2[1]
   assert s2[3]._navigator._prevBead is s2[2]


def test_bead_navigation_33( ):
   '''nextBead and prevBead DO work in sequence of arbitrarily nexted sequentials.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(2)])
   s2 = Sequential([Note(i, (1,8)) for i in range(3,5)])
   v = Voice([s1, Note(2, (1,8)), s2])
   assert s1[1]._navigator._nextBead is v[1]
   assert v[1]._navigator._nextBead is s2[0]

   assert v[1]._navigator._prevBead is s1[1]
   assert s2[0]._navigator._prevBead is v[1]

### Parentage asymmetrical structures DON'T work if NOT tautological ###

def test_bead_navigation_34( ):
   '''NextBead returns None in asymmetric thread parentage structurese.'''
   v1 = Voice([Note(i , (1,8)) for i in range(3)])
   n = Note(3, (1,8))
   v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
   t = Staff([v1, n, v2])
   assert v1[-1]._navigator._nextBead is None
   assert n._navigator._nextBead is None

   assert v2[0]._navigator._prevBead is None
   assert n._navigator._prevBead is None


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

   assert v3[0]._navigator._prevBead is None
   assert v2[0]._navigator._prevBead is None


### TAUTOLOGICAL NESTING ###

def test_bead_navigation_50a( ):
   '''nextBead and prevBead work on nested anonymous Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(3)])
   vout = Voice([vin, Note(3, (1,8))])
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vin[2]._navigator._nextBead is vout[1]

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vout[1]._navigator._prevBead is vin[-1]


def test_bead_navigation_50b( ):
   '''nextBead and prevBead work on nested anonymous Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(1,4)])
   vout = Voice([Note(0, (1,8)), vin])
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vout[0]._navigator._nextBead is vin[0]

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vin[0]._navigator._prevBead is vout[0]


def test_bead_navigation_51a( ):
   '''nextBead and prevBead work on nested equally named Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(3)])
   vin.invocation.name = 'myvoice'
   vout = Voice([vin, Note(3, (1,8))])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vin[2]._navigator._nextBead is vout[1]

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vout[1]._navigator._prevBead is vin[-1]


def test_bead_navigation_51b( ):
   '''nextBead and prevBead work on nested equally named Voices.'''
   vin = Voice([Note(i, (1,8)) for i in range(1,4)])
   vin.invocation.name = 'myvoice'
   vout = Voice([Note(0, (1,8)), vin])
   vout.invocation.name = 'myvoice'
   assert vin[0]._navigator._nextBead is vin[1]
   assert vin[1]._navigator._nextBead is vin[2]
   assert vout[0]._navigator._nextBead is vin[0]

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vin[0]._navigator._prevBead is vout[0]


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

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vout[1]._navigator._prevBead is None


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

   assert vin[1]._navigator._prevBead is vin[0]
   assert vin[2]._navigator._prevBead is vin[1]
   assert vout[1]._navigator._prevBead is None


### NEXT LEAVES ###

def test_nextLeaves_navigation_01( ):
   '''nextLeaves works on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves == [t[1]]
   assert t[1]._navigator._nextLeaves == [t[2]]
   assert t[2]._navigator._nextLeaves == [t[3]]
   assert t[3]._navigator._nextLeaves is None


def test_nextLeaves_navigation_02( ):
   '''NextLeaf works on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves == [t[1]]
   assert t[1]._navigator._nextLeaves == [t[2]]
   assert t[2]._navigator._nextLeaves == [t[3]]
   assert t[3]._navigator._nextLeaves is None

def test_nextLeaves_navigation_03( ):
   '''NextLeaf works on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves is None
   assert t[1]._navigator._nextLeaves is None
   assert t[2]._navigator._nextLeaves is None
   assert t[3]._navigator._nextLeaves is None

### LEVEL 1 NESTING ###

def test_nextLeaves_navigation_10( ):
   '''nextLeaves works on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s1[0]._navigator._nextLeaves == [s1[1]]
   assert s1[1]._navigator._nextLeaves == [s1[2]]
   assert s1[2]._navigator._nextLeaves == [s1[3]]
   assert s1[3]._navigator._nextLeaves == [s2[0]]

def test_nextLeaves_navigation_11( ):
   '''nextLeaves works on contiguous Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextLeaves == [v1[1]]
   assert v1[1]._navigator._nextLeaves == [v1[2]]
   assert v1[2]._navigator._nextLeaves == [v1[3]]
   assert v1[3]._navigator._nextLeaves == [v2[0]]

### LEVEL 2 NESTING ###

def test_nextLeaves_navigation_20( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   assert v1[3]._navigator._nextLeaves == [v2[0]]
   assert v1._navigator._nextLeaves == [v2[0]]
   

def test_nextLeaves_navigation_21( ):
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])

   s1 = Staff([vh1, vl1])
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.brackets = 'double-angle'

   seq = Sequential([s1, s2])

   assert vl1[3]._navigator._nextLeaves == [vl2[0], vh2[0]]
   assert vh1[3]._navigator._nextLeaves == [vl2[0], vh2[0]]
   assert vh1._navigator._nextLeaves  == [vl2[0], vh2[0]]
   assert vl1._navigator._nextLeaves  == [vl2[0], vh2[0]]



### PREVIOUS LEAVES ###

def test_prevLeaves_navigation_01( ):
   '''prevLeaves works on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves == [t[0]]
   assert t[2]._navigator._prevLeaves == [t[1]]
   assert t[3]._navigator._prevLeaves == [t[2]] 


def test_prevLeaves_navigation_02( ):
   '''prevLeaves works on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves == [t[0]]
   assert t[2]._navigator._prevLeaves == [t[1]]
   assert t[3]._navigator._prevLeaves == [t[2]]

def test_prevLeaves_navigation_03( ):
   '''prevLeaves works on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves is None
   assert t[2]._navigator._prevLeaves is None
   assert t[3]._navigator._prevLeaves is None

### LEVEL 1 NESTING ###

def test_prevLeaves_navigation_10( ):
   '''prevLeaves works on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s2[0]._navigator._prevLeaves == [s1[3]]
   assert s2._navigator._prevLeaves == [s1[3]]
   assert s1[0]._navigator._prevLeaves is None

def test_prevLeaves_navigation_11( ):
   '''prevLeaves works on contiguous Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v2[0]._navigator._prevLeaves == [v1[3]]
   assert v2._navigator._prevLeaves == [v1[3]]
   assert v1[0]._navigator._prevLeaves is None

### LEVEL 2 NESTING ###

def test_prevLeaves_navigation_20( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   assert v2[0]._navigator._prevLeaves == [v1[3]]
   assert v2._navigator._prevLeaves == [v1[3]]
   assert s2._navigator._prevLeaves == [v1[3]]
   

def test_prevLeaves_navigation_21( ):
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])

   s1 = Staff([vh1, vl1])
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.brackets = 'double-angle'

   seq = Sequential([s1, s2])

   assert vl2[0]._navigator._prevLeaves == [vh1[3], vl1[3]]
   assert vh2[0]._navigator._prevLeaves == [vh1[3], vl1[3]]
   assert vl2._navigator._prevLeaves  == [vh1[3], vl1[3]]
   assert vh2._navigator._prevLeaves  == [vh1[3], vl1[3]]
