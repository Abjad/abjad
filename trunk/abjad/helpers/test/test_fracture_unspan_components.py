from abjad import *
import py.test


def test_fracture_unspan_components_01( ):
   '''Fracture to the left of the leftmost component in list;
      fracture to the right of the rightmost component in list;
      unspan all components in list.'''

   t = Staff(scale(4))
   Beam(t[:])
   fracture_unspan_components(t[1:3])

   r'''
   \new Staff {
      c'8 [ ]
      d'8
      e'8
      f'8 [ ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8\n\te'8\n\tf'8 [ ]\n}"
   

def test_fracture_unspan_components_02( ):
   '''Fracture to the left of the leftmost component in list;
      fracture to the right of the rightmost component in list;
      unspan all components in list.'''

   t = Staff(scale(4))
   Beam(t[:])
   fracture_unspan_components(t[1:2])

   r'''
   \new Staff {
      c'8 [ ]
      d'8
      e'8 [
      f'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8\n\te'8 [\n\tf'8 ]\n}"


def test_fracture_unspan_components_03( ):
   '''Empty list raises no exception.'''

   result = fracture_unspan_components([ ])
   assert result == [ ]


def test_fracture_unspan_components_04( ):
   '''Nonsuccessive components raise ContiguityError.'''

   t1 = Staff(scale(4))
   t2 = Staff(scale(4))
   assert py.test.raises(
      ContiguityError, 'fracture_unspan_components(t1[:] + t2[:])')
