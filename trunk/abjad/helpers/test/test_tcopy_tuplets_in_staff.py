from abjad import *


### TODO - implement some sort of 'crossing' copy.
### given t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
### there is currently no way to copy, eg, leaves 0 - 5
### because leaves 0 - 3 belong to tuplet 0 
### while leaves 4 - 5 belong to tuplet 1;
### in other words, leaves 0 - 5 'cross' tuplet boundaries.
### not sure what the right interface here would be;
### it isn't possible to say t.leaves(0, 5) because t.leaves
### is merely a (built-in) list.
### this may motivate a (non-OOP) copy( ) function;
### then copy(t, (0, 5), indices = 'leaves') might make sense;
### or leafCopy(t, (0, 5)), or something similar.

def test_tcopy_tuplets_in_staff_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[0:1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration.preprolated == t[0].duration.preprolated
   assert id(u[0]) is not id(t[0])
   assert u[0]._parent == u
   

def test_tcopy_tuplets_in_staff_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1:2])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration.preprolated == t[1].duration.preprolated
   assert id(u[0]) is not id(t[1])
   assert u[0]._parent == u
   

def test_tcopy_tuplets_in_staff_03( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[-1:])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration.preprolated == t[-1].duration.preprolated
   assert id(u[0]) is not id(t[-1])
   assert u[0]._parent == u


def test_tcopy_tuplets_in_staff_04( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[-2:-1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration.preprolated == t[-2].duration.preprolated
   assert id(u[0]) is not id(t[-2])
   assert u[0]._parent == u
