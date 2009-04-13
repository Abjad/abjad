from abjad import *


def test_containertools_contents_multiply_01( ):
   '''Multiply notes in voice.'''

   t = Voice(scale(2))
   Beam(t[:])
   containertools.contents_multiply(t, total = 3)

   r'''\new Voice {
           c'8 [
           d'8 ]
           c'8 [
           d'8 ]
           c'8 [
           d'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_contents_multiply_02( ):
   '''Multiplication by one leaves contents unchanged.'''

   t = Voice(scale(2))
   Beam(t[:])
   containertools.contents_multiply(t, total = 1)

   r'''\new Voice {
           c'8 [
           d'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_contents_multiply_03( ):
   '''Multiplication by zero empties container.'''
   
   t = Voice(scale(2))
   Beam(t[:])
   containertools.contents_multiply(t, total = 0)

   r'''\new Voice {
   }'''

   assert check.wf(t)
   assert t.format == '\\new Voice {\n}'
