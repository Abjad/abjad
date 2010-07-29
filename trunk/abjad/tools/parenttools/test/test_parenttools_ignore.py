from abjad import *
from abjad.tools.parenttools.ignore import _ignore


def test_parenttools_ignore_01( ):

   t = Voice(macros.scale(4))
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

   assert (t[0], t) in receipt
   assert (t[1], t) in receipt
   assert (t[2], t) in receipt
   assert (t[3], t) in receipt

   "Follow soon after with parenttools.restore(receipt)."
