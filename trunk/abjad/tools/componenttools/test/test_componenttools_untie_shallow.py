from abjad import *


def test_componenttools_untie_shallow_01( ):
   t = Staff(construct.notes(0, [(5, 16), (5, 16)]))

   r'''
   \new Staff {
      c'4 ~
      c'16
      c'4 ~
      c'16
   }
   '''
   
   componenttools.untie_shallow(t[:])

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


def test_componenttools_untie_shallow_02( ):
   '''Handles empty list without exception.'''

   result = componenttools.untie_shallow([ ])
   assert result == [ ]
