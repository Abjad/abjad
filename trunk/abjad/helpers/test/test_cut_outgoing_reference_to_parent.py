from abjad import *
from abjad.helpers.cut_outgoing_reference_to_parent import \
   _cut_outgoing_reference_to_parent


def test_cut_outgoing_reference_to_parent_01( ):

   t = Voice(scale(4))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   receipt = _cut_outgoing_reference_to_parent(t[:])

   assert not check(t)

   assert (t[0], t) in receipt
   assert (t[1], t) in receipt
   assert (t[2], t) in receipt
   assert (t[3], t) in receipt

   "Follow soon after with _restore_outgoing_reference_to_parent(receipt)."
