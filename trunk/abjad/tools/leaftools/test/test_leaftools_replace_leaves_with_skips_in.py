from abjad import *


def test_leaftools_replace_leaves_with_skips_in_01( ):
   '''Works on Abjad components.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   leaftools.replace_leaves_with_skips_in(t)

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


def test_leaftools_replace_leaves_with_skips_in_02( ):
   '''Works on Python lists of Abjad components.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   leaftools.replace_leaves_with_skips_in(t[:])

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
