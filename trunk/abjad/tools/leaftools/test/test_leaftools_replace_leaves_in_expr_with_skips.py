from abjad import *


def test_leaftools_replace_leaves_in_expr_with_skips_01( ):
   '''Works on Abjad components.'''

   t = Staff(macros.scale(4))
   leaftools.replace_leaves_in_expr_with_skips(t)

   r'''
   \new Staff {
      s8
      s8
      s8
      s8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\ts8\n\ts8\n\ts8\n\ts8\n}'


def test_leaftools_replace_leaves_in_expr_with_skips_02( ):
   '''Works on Python lists of Abjad components.'''

   t = Staff(macros.scale(4))
   leaftools.replace_leaves_in_expr_with_skips(t[:])

   r'''
   \new Staff {
      s8
      s8
      s8
      s8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\ts8\n\ts8\n\ts8\n\ts8\n}'
