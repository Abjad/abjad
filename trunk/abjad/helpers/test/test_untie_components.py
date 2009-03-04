from abjad import *
from abjad.tools import construct


def test_untie_components_01( ):
   t = Staff(construct.notes(0, [(5, 16), (5, 16)]))

   r'''
   \new Staff {
      c'4 ~
      c'16
      c'4 ~
      c'16
   }
   '''
   
   untie_components(t[:])

   r'''
   \new Staff {
      c'4
      c'16
      c'4
      c'16
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'4\n\tc'16\n\tc'4\n\tc'16\n}"


def test_untie_components_02( ):
   '''Handles empty list without exception.'''

   result = untie_components([ ])
   assert result == [ ]
