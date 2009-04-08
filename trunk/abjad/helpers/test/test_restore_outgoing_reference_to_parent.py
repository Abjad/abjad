from abjad import *
from abjad.helpers.ignore_parent import \
   _ignore_parent
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent


def test_restore_outgoing_reference_to_parent_01( ):

   t = Voice(scale(4))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   receipt = _ignore_parent(t[:])

   assert not check(t)

   restore_outgoing_reference_to_parent(receipt)

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''
  
   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
