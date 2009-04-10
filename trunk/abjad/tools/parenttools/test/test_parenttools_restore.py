from abjad import *


def test_parenttools_restore_01( ):

   t = Voice(scale(4))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   receipt = parenttools.ignore_parent(t[:])

   assert not check(t)

   parenttools.restore(receipt)

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''
  
   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
