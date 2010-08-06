from abjad import *


def test_tietools_remove_tie_spanner_from_components_tmp_01( ):
   t = Staff(leaftools.make_notes(0, [(5, 16), (5, 16)]))

   r'''
   \new Staff {
      c'4 ~
      c'16
      c'4 ~
      c'16
   }
   '''
   
   tietools.remove_tie_spanner_from_components_tmp(t[:])

   r'''
   \new Staff {
      c'4
      c'16
      c'4
      c'16
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'4\n\tc'16\n\tc'4\n\tc'16\n}"


def test_tietools_remove_tie_spanner_from_components_tmp_02( ):
   '''Handles empty list without exception.'''

   result = tietools.remove_tie_spanner_from_components_tmp([ ])
   assert result == [ ]
