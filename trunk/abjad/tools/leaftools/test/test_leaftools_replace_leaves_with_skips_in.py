from abjad import *


def test_leaftools_replace_leaves_with_skips_in_01( ):
   '''Works on Abjad components.'''

   t = Staff(construct.scale(4))
   leaftools.replace_leaves_with_skips_in(t)

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


def test_leaftools_replace_leaves_with_skips_in_02( ):
   '''Works on Python lists of Abjad components.'''

   t = Staff(construct.scale(4))
   leaftools.replace_leaves_with_skips_in(t[:])

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
