from abjad import *


def test_leaftools_multiply_01( ):
   '''Multiply each leaf in voice by 1.'''

   t = Voice(construct.scale(3))
   p = Beam(t[:])
   leaftools.multiply(t, total = 2)

   r'''\new Voice {
      c'8 [
      c'8
      d'8
      d'8
      e'8
      e'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\td'8\n\td'8\n\te'8\n\te'8 ]\n}"


def test_leaftools_multiply_02( ):
   '''Multiply each leaf in voice by 2.'''

   t = Voice(construct.scale(3))
   Beam(t[:])
   leaftools.multiply(t, total = 3)

   r'''\new Voice {
      c'8 [
      c'8
      c'8
      d'8
      d'8
      d'8
      e'8
      e'8
      e'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\tc'8\n\td'8\n\td'8\n\td'8\n\te'8\n\te'8\n\te'8 ]\n}"
