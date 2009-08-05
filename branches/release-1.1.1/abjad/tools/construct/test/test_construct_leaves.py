from abjad import *
from abjad.tools import construct

def test_construct_leaves_01( ):
   '''
   Leaves constructor can create chords, notes and rests simultaneously.
   '''
   leaves = construct.leaves([1, (1,2,3), None], [(1, 4)])
   assert isinstance(leaves[0], Note) 
   assert isinstance(leaves[1], Chord) 
   assert isinstance(leaves[2], Rest) 
   for l in leaves:
      assert l.duration.written == Rational(1, 4)


def test_construct_leaves_02( ):
   '''
   Leaves constructor can create prolated chords, notes and rests 
   simultaneously. Contiguous leaves with the same prolation are
   put together inside a Tuplet.
   '''
   leaves = construct.leaves([1, (1,2,3), None], [(2, 9), (1,18), (1,5)])
   assert isinstance(leaves[0], FixedMultiplierTuplet)
   assert isinstance(leaves[1], FixedMultiplierTuplet)
   tuplet1 = leaves[0] 
   assert len(tuplet1) == 2
   assert tuplet1.duration.multiplier == Rational(8, 9)
   assert isinstance(tuplet1[0], Note) 
   assert isinstance(tuplet1[1], Chord) 
   tuplet2 = leaves[1] 
   assert len(tuplet2) == 1
   assert tuplet2.duration.multiplier == Rational(4, 5)
   assert isinstance(tuplet2[0], Rest) 

   assert tuplet1[0].duration.written == Rational(2, 8)
   assert tuplet1[1].duration.written == Rational(1, 16)
   assert tuplet2[0].duration.written == Rational(1, 4)


def test_construct_leaves_03( ):
   '''
   Leaves constructor can create prolated and unprolated chords, 
   notes and rests simultaneously. 
   '''
   leaves = construct.leaves([1, (1,2,3), None], [(2, 9), (1,8), (1,5)])
   assert isinstance(leaves[0], FixedMultiplierTuplet)
   assert isinstance(leaves[1], Chord)
   assert isinstance(leaves[2], FixedMultiplierTuplet)
   tuplet1 = leaves[0] 
   assert len(tuplet1) == 1
   assert tuplet1.duration.multiplier == Rational(8, 9)
   assert isinstance(tuplet1[0], Note) 
   tuplet2 = leaves[2] 
   assert len(tuplet2) == 1
   assert tuplet2.duration.multiplier == Rational(4, 5)
   assert isinstance(tuplet2[0], Rest) 


def test_construct_leaves_04( ):
   '''Leaves constructor can take an optional 'tied_rests' keyword argument.'''
   leaves = construct.leaves([None], [(5, 32), (5, 32)], tied_rests=True)
   assert len(leaves) == 4
   for l in leaves:
      assert isinstance(l, Rest)
   assert leaves[0].tie.spanner is leaves[1].tie.spanner
   assert leaves[2].tie.spanner is leaves[3].tie.spanner


def test_construct_leaves_05( ):
   ''''tied_rests' is False by default.'''
   leaves = construct.leaves([None], [(5, 32), (5, 32)])
   assert len(leaves) == 4
   for l in leaves:
      assert isinstance(l, Rest)
      assert l.tie.spanned == False
