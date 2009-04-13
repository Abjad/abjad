from abjad import *


def test_flip_01( ):
   '''Flip leaf under continuous spanner.'''

   t = Voice(construct.scale(4))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   flip(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8
      d'8
      f'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\td'8\n\tf'8 ]\n}"


def test_flip_02( ):
   '''Flip leaf across spanner boundaries.'''

   t = Voice(construct.scale(4))
   Beam(t[:2])
   Beam(t[2:])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8 [
      f'8 ]
   }
   '''

   flip(t[1])
   
   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8 [
      f'8 ]
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8 [\n\tf'8 ]\n}"


def test_flip_03( ):
   '''Flip leaf from within to without spanner.'''

   t = Voice(construct.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   flip(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8\n\tf'8\n}"
