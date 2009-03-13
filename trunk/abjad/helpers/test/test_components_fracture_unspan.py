from abjad import *
import py.test


def test_components_fracture_unspan_01( ):
   '''Fracture to the left of the leftmost component in list;
      fracture to the right of the rightmost component in list;
      unspan all components in list.'''

   t = Staff(scale(4))
   Beam(t[:])
   components_fracture_unspan(t[1:3])

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
   

def test_components_fracture_unspan_02( ):
   '''Fracture to the left of the leftmost component in list;
      fracture to the right of the rightmost component in list;
      unspan all components in list.'''

   t = Staff(scale(4))
   Beam(t[:])
   components_fracture_unspan(t[1:2])

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


def test_components_fracture_unspan_03( ):
   '''Empty list raises no exception.'''

   result = components_fracture_unspan([ ])
   assert result == [ ]


def test_components_fracture_unspan_04( ):
   '''Nonsuccessive components raise ContiguityError.'''

   t1 = Staff(scale(4))
   t2 = Staff(scale(4))
   assert py.test.raises(
      ContiguityError, 'components_fracture_unspan(t1[:] + t2[:])')
