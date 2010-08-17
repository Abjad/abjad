from abjad import *


def test_leaftools_scale_preprolated_leaf_duration_01( ):

   t = Note(0, (1, 4))
   leaftools.scale_preprolated_leaf_duration(t, Rational(1, 2))
   assert t.format == "c'8"


def test_leaftools_scale_preprolated_leaf_duration_02( ):

   t = Note(0, (1, 4))
   leaftools.scale_preprolated_leaf_duration(t, Rational(2))
   assert t.format == "c'2"


def test_leaftools_scale_preprolated_leaf_duration_03( ):

   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   leaftools.scale_preprolated_leaf_duration(staff[1], Rational(5, 4))

   r'''
   \new Staff {
           c'8 [
           d'8 ~
           d'32
           e'8
           f'8 ]
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8 ~\n\td'32\n\te'8\n\tf'8 ]\n}"


def test_leaftools_scale_preprolated_leaf_duration_04( ):

   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   leaftools.scale_preprolated_leaf_duration(staff[1], Rational(2, 3))

   r'''
   \new Staff {
           c'8 [
           \times 2/3 {
                   d'8
           }
           e'8
           f'8 ]
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'8\n\t}\n\te'8\n\tf'8 ]\n}"
