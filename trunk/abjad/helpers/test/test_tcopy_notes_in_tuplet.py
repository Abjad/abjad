from abjad import *


### COPY ADJACENT TUPLETIZED NOTES ###
### note - right now notes get 'ripped' out of tuplets
### and so lose parentage;
### the key assertion that shows this is 
### x.duratum != y.duratum;
### a different type of copy would preserve parentage
### and 'cut' out a (partial) tuplet to return;
### eg, cutting the first two notes of a triplet would
### return a broken tuplet equal to 2/12.
### TODO - that functionality does not yet exist
### but should implement somewhere;
### the question is what the appropriate interface should be;
### maybe copy(t, (0, 1), mode = 'preserve partial tuplets') or
### a different verb like excise(t, (0, 1)).

def test_tcopy_notes_in_tuplet_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1][0:2])
   assert isinstance(u, FixedDurationTuplet)
   assert len(u) == 2
   for i, x in enumerate(u):
      j = i + 0
      assert x.pitch.number == t[1][j].pitch.number
      assert id(x) != id(t[1][j])
   assert check(u)


def test_tcopy_notes_in_tuplet_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1][1:3])
   assert isinstance(u, FixedDurationTuplet)
   assert len(u) == 2
   for i, x in enumerate(u):
      j = i + 1
      assert x.pitch.number == t[1][j].pitch.number
      assert id(x) != id(t[1][j])
   assert check(u)
