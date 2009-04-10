from abjad import *
import py.test


def test_durtools_sum_preprolated_01( ):
   '''Return sum of preprolated duration of components in list.'''
   
   t = FixedDurationTuplet((2, 8), scale(3))

   assert durtools.sum_preprolated(t[:]) == Rational(3, 8)


def test_durtools_sum_preprolated_02( ):
   '''Return zero for empty list.'''

   assert durtools.sum_preprolated([ ]) == Rational(0)


def test_durtools_sum_preprolated_03( ):
   '''Raise ContiguityError for components not in same parent.'''

   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   pitchtools.diatonicize(t)

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
      'durtools.sum_preprolated(t.leaves)')
