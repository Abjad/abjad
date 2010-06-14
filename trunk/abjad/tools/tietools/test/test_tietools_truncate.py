from abjad import *


def test_tietools_truncate_01( ):
   '''Keep and unspan first note in tie chain only.'''

   t = Staff(leaftools.make_notes(0, [(5, 16)]))

   r'''
   \new Staff {
      c'4 ~
      c'16
   }
   '''
   
   tietools.truncate(t[0].tie.chain)

   r'''
   \new Staff {
      c'4
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'4\n}"


def test_tietools_truncate_02( ):
   '''No effect on length-1 tie chains.'''

   t = Staff(leaftools.make_repeated_notes(1))

   tietools.truncate(t[0].tie.chain)

   r'''
   \new Staff {
      c'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n}"
