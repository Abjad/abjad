from abjad import *
import py.test


def test_componenttools_get_duration_preprolated_01( ):
   '''Return sum of preprolated duration of components in list.'''
   
   t = FixedDurationTuplet((2, 8), scale(3))

   assert componenttools.get_duration_preprolated(t[:]) == Rational(3, 8)


def test_componenttools_get_duration_preprolated_02( ):
   '''Return zero for empty list.'''

   assert componenttools.get_duration_preprolated([ ]) == Rational(0)


def test_componenttools_get_duration_preprolated_03( ):
   '''Raise ContiguityError for components not in same parent.'''

   t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
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
      'componenttools.get_duration_preprolated(t.leaves)')
