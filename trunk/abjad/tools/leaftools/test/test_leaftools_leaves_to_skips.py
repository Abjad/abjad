from abjad import *


def test_leaftools_leaves_to_skips_01( ):
   '''Works on Abjad components.'''

   t = Staff(construct.scale(4))
   leaftools.leaves_to_skips(t)

   r'''
   \new Staff {
      s8
      s8
      s8
      s8
   }
   '''

   assert check.wf(t)
   assert t.format == '\\new Staff {\n\ts8\n\ts8\n\ts8\n\ts8\n}'


def test_leaftools_leaves_to_skips_02( ):
   '''Works on Python lists of Abjad components.'''

   t = Staff(construct.scale(4))
   leaftools.leaves_to_skips(t[:])

   r'''
   \new Staff {
      s8
      s8
      s8
      s8
   }
   '''

   assert check.wf(t)
   assert t.format == '\\new Staff {\n\ts8\n\ts8\n\ts8\n\ts8\n}'
