from abjad import *

def test_leaf_split_01( ):
   '''Split duration equals 0. Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split(0, t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 4)
   assert new[0] == t

def test_leaf_split_02( ):
   '''Split duration >= Leaf duration. Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split((3, 4), t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 4)
   assert new[0] == t

def test_leaf_split_03( ):
   '''Slit returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split((1, 8), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 8)
   assert isinstance(new[1], Note)
   assert new[1].duration == Rational(1, 8)


def test_leaf_split_04( ):
   '''Split returns two FixedDurationTuplets.'''
   ### TODO: I think this should return a single tuplet. 
   ### i.e. these two tuplets should be fused into one. 
   t = Note(0, (1, 4))
   new = leaf_split((1, 12), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], FixedDurationTuplet)
   #assert new[0].duration == Rational(1, 12)
   assert new[0].duration.target == Rational(1, 12)
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration == Rational(1, 8)
   assert isinstance(new[1], FixedDurationTuplet)
   #assert new[1].duration == Rational(1, 6)
   assert new[1].duration.target == Rational(1, 6)
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration == Rational(1, 4)


