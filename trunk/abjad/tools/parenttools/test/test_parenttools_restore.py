from abjad import *
from abjad.tools.parenttools.ignore import _ignore
from abjad.tools.parenttools.restore import _restore


def test_parenttools_restore_01( ):

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   receipt = _ignore(t[:])

   assert not componenttools.is_well_formed_component(t)

   _restore(receipt)

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''
  
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
