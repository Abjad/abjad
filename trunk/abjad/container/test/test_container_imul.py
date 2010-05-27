from abjad import *


def test_container_imul_01( ):

   t = Voice(construct.scale(2))
   Beam(t[:])
   t *= 2

   r'''
   \new Voice {
           c'8 [
           d'8 ]
           c'8 [
           d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n}"


def test_container_imul_02( ):

   t = Voice(construct.scale(2))
   Beam(t[:])
   t *= 1

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_imul_03( ):

   t = Voice(construct.scale(2))
   Beam(t[:])
   t *= 0

   r'''
   \new Voice {
   }
   '''
   
   assert check.wf(t)
   assert t.format == '\\new Voice {\n}'
