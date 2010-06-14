from abjad import *


def test_componenttools_remove_tie_spanners_from_components_01( ):
   t = Staff(leaftools.make_notes(0, [(5, 16), (5, 16)]))

   r'''
   \new Staff {
      c'4 ~
      c'16
      c'4 ~
      c'16
   }
   '''
   
   componenttools.remove_tie_spanners_from_components(t[:])

   r'''
   \new Staff {
      c'4
      c'16
      c'4
      c'16
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'4\n\tc'16\n\tc'4\n\tc'16\n}"


def test_componenttools_remove_tie_spanners_from_components_02( ):
   '''Handles empty list without exception.'''

   result = componenttools.remove_tie_spanners_from_components([ ])
   assert result == [ ]
