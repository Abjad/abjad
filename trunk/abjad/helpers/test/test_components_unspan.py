from abjad import *


def test_components_unspan_01( ):
   t = Staff(scale(4))
   Beam(t[:])
   components_unspan(t[:])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_components_unspan_02( ):
   t = Staff(scale(4))
   Beam(t[:])
   components_unspan(t[0:2])

   r'''
   \new Staff {
      c'8
      d'8 
      e'8 [
      f'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8 [\n\tf'8 ]\n}"


def test_components_unspan_03( ):
   t = components_unspan([ ])
   assert t == [ ]
