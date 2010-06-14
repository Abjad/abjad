from abjad import *
import py.test


def test_componenttools_get_preprolated_duration_of_components_01( ):
   '''Return sum of preprolated duration of components in list.'''
   
   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))

   assert componenttools.get_preprolated_duration_of_components(t[:]) == Rational(3, 8)


def test_componenttools_get_preprolated_duration_of_components_02( ):
   '''Return zero for empty list.'''

   assert componenttools.get_preprolated_duration_of_components([ ]) == Rational(0)


def test_componenttools_get_preprolated_duration_of_components_03( ):
   '''Raise ContiguityError for components not in same parent.'''

   t = Voice(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
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
   }
   '''

   assert py.test.raises(ContiguityError,
      'componenttools.get_preprolated_duration_of_components(t.leaves)')
