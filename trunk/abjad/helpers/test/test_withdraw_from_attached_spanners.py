from abjad import *
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners


def test_withdraw_from_attached_spanners_01( ):
   t = Staff(scale(4))
   Beam(t[:])
   _withdraw_from_attached_spanners(t[:])

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_withdraw_from_attached_spanners_02( ):
   t = Staff(scale(4))
   Beam(t[:])
   _withdraw_from_attached_spanners(t[0:2])

   r'''\new Staff {
      c'8
      d'8 
      e'8 [
      f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8 [\n\tf'8 ]\n}"


def test_withdraw_from_attached_spanners_03( ):
   t = _withdraw_from_attached_spanners([ ])
   assert t == [ ]
