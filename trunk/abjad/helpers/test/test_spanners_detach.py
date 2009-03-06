from abjad import *


def test_spanners_detach_01( ):
   '''Detach spanners from all components in expr.'''

   t = Voice(scale(4))
   Beam(t[:])
   spanners_detach([t], level = 'all')

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spanners_detach_02( ):
   '''Detach spanners from all components in expr.'''

   t = Voice(scale(4))
   Beam(t)
   spanners_detach([t], level = 'all')

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spanners_detach_03( ):
   '''Detach spanners from components at top level of expr only.'''

   t = Voice(scale(4))
   Beam(t[:])
   spanners_detach([t], level = 'top')

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_spanners_detach_04( ):
   '''Detach spanners from components at top level of expr only.'''

   t = Voice(scale(4))
   Beam(t)
   spanners_detach([t], level = 'top')

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
