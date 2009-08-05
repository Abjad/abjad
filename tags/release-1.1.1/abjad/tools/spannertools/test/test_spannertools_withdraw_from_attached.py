from abjad import *
from abjad.tools.spannertools.withdraw_from_attached import \
   _withdraw_from_attached


def test_spannertools_withdraw_from_attached_01( ):
   t = Staff(construct.scale(4))
   Beam(t[:])
   _withdraw_from_attached(t[:])

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spannertools_withdraw_from_attached_02( ):
   t = Staff(construct.scale(4))
   Beam(t[:])
   _withdraw_from_attached(t[0:2])

   r'''\new Staff {
      c'8
      d'8 
      e'8 [
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8 [\n\tf'8 ]\n}"


def test_spannertools_withdraw_from_attached_03( ):
   t = _withdraw_from_attached([ ])
   assert t == [ ]
