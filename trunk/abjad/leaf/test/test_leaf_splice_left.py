from abjad import *


def test_leaf_splice_left_01( ):
   '''Splice leaves left of leaf.'''

   t = Voice(scale(3))
   Beam(t[:])
   result = t[0].splice_left(scale(3, Rational(1, 16)))

   r'''\new Voice {
           c'16 [
           d'16
           e'16
           c'8
           d'8
           e'8 ]
   }'''
   
   assert check.wf(t)
   assert result == t[:4]
   assert t.format == "\\new Voice {\n\tc'16 [\n\td'16\n\te'16\n\tc'8\n\td'8\n\te'8 ]\n}"


def test_leaf_splice_left_02( ):
   '''Splice leaf left of interior leaf.'''

   t = Voice(scale(3))
   Beam(t[:])
   result = t[1].splice_left([Note(1.5, (1, 8))])

   r'''\new Voice {
           c'8 [
           dqf'8
           d'8
           e'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
   assert result == t[1:3]
