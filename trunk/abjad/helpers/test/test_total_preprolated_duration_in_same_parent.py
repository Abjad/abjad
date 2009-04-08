from abjad.helpers.total_preprolated_duration_in_same_parent import _total_preprolated_duration_in_same_parent
from abjad import *
import py.test


def test_total_preprolated_duration_in_same_parent_01( ):
   '''Return sum of preprolated duration of components in list.'''
   
   t = FixedDurationTuplet((2, 8), scale(3))

   assert _total_preprolated_duration_in_same_parent(t[:]) == Rational(3, 8)


def test_total_preprolated_duration_in_same_parent_02( ):
   '''Return zero for empty list.'''

   assert _total_preprolated_duration_in_same_parent([ ]) == Rational(0)


def test_total_preprolated_duration_in_same_parent_03( ):
   '''Raise ContiguityError for components not in same parent.'''

   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   pitches.diatonicize(t)

   r'''\new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }'''

   assert py.test.raises(ContiguityError,
      '_total_preprolated_duration_in_same_parent(t.leaves)')
