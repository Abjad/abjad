from abjad import *

def test_leaf_split_binary_01( ):
   '''Split duration equals 0. Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary(0, t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 4)
   assert new[0] == t

def test_leaf_split_binary_02( ):
   '''Split duration >= Leaf duration. Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((3, 4), t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 4)
   assert new[0] == t

def test_leaf_split_binary_03( ):
   '''Slit returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((1, 8), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 8)
   assert isinstance(new[1], Note)
   assert new[1].duration == Rational(1, 8)


def test_leaf_split_binary_04( ):
   '''Split returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((1, 16), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(1, 16)
   assert isinstance(new[1], Note)
   assert new[1].duration == Rational(3, 16)

def test_leaf_split_binary_05( ):
   '''Split returns three Leaves, two are tied.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((5, 32), t)
   assert isinstance(new, list)
   assert len(new) == 3
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(4, 32)
   assert new[0].tie == True
   assert isinstance(new[1], Note)
   assert new[1].duration == Rational(1, 32)
   assert new[1].tie == False
   assert isinstance(new[2], Note)
   assert new[2].duration == Rational(3, 32)
   assert new[2].tie == False

