from abjad import *


def test_leaf_split_01( ):
   '''Split duration equals 0. 
      Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split(t, Rational(0))
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration.written == Rational(1, 4)
   assert new[0] == t


def test_leaf_split_02( ):
   '''Split duration >= Leaf duration. 
      Leaf is not split and is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split(t, Rational(3, 4))
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration.written == Rational(1, 4)
   assert new[0] == t


def test_leaf_split_03( ):
   '''Split returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split(t, Rational(1, 8))
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Note)
   assert new[1].duration.written == Rational(1, 8)


def test_leaf_split_04( ):
   '''Split returns two FixedDurationTuplets.'''
   t = Note(0, (1, 4))
   new = leaf_split(t, Rational(1, 12))
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], FixedDurationTuplet)
   assert new[0].duration.target == Rational(1, 12)
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration.written == Rational(1, 8)
   assert isinstance(new[1], FixedDurationTuplet)
   assert new[1].duration.target == Rational(1, 6)
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration.written == Rational(1, 4)


def test_leaf_split_05( ):
   '''Split spanned leaf with spanner 
      crossing container boundaries.'''

   t = Voice(run(1) + [FixedDurationTuplet((2, 8), run(3))])
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''\new Voice {
      c'8 [
      \times 2/3 {
         d'8
         e'8
         f'8 ]
      }
   }'''

   leaf_split(t.leaves[1], Rational(1, 24))

   r'''\new Voice {
      c'8 [
      \times 2/3 {
         d'16
         d'16
         e'8
         f'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'16\n\t\td'16\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
