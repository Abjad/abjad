from abjad import *
from abjad.components._Leaf import _Leaf


def test_componenttools_iterate_components_backward_in_expr_01( ):
   '''Yield nothing when class not present.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = componenttools.iterate_components_backward_in_expr(t, Rest)
   assert len(list(iter)) == 0


def test_componenttools_iterate_components_backward_in_expr_02( ):
   '''Yield topmost node only.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = componenttools.iterate_components_backward_in_expr(t, Staff)
   assert len(list(iter)) == 1


def test_componenttools_iterate_components_backward_in_expr_03( ):
   '''Yield internal nodes only.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = componenttools.iterate_components_backward_in_expr(t, Tuplet)
   assert len(list(iter)) == 3


def test_componenttools_iterate_components_backward_in_expr_04( ):
   '''Yield exact leaves.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = componenttools.iterate_components_backward_in_expr(t, Note)
   assert len(list(iter)) == 9


def test_componenttools_iterate_components_backward_in_expr_05( ):
   '''Yield leaves based on names higher in inheritence hierarchy.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.components._Leaf import _Leaf
   iter = componenttools.iterate_components_backward_in_expr(t, _Leaf)
   assert len(list(iter)) == 9


def test_componenttools_iterate_components_backward_in_expr_06( ):
   '''Yield all nodes in tree.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.components._Component._Component import _Component
   iter = componenttools.iterate_components_backward_in_expr(t, _Component)
   assert len(list(iter)) == 13


def test_componenttools_iterate_components_backward_in_expr_07( ):
   '''Yield all all python objects.'''
   t = Staff(tuplettools.FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = componenttools.iterate_components_backward_in_expr(t, object)
   assert len(list(iter)) == 13


def test_componenttools_iterate_components_backward_in_expr_08( ):
   '''From backward start index.'''

   t = Staff(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
   macros.diatonicize(t)

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   leaves = list(componenttools.iterate_components_backward_in_expr(t, _Leaf, 3))

   assert leaves[0] is t.leaves[2]
   assert leaves[1] is t.leaves[1]
   assert leaves[2] is t.leaves[0]


def test_componenttools_iterate_components_backward_in_expr_09( ):
   '''To backward stop index.'''

   t = Staff(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
   macros.diatonicize(t)

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   leaves = list(componenttools.iterate_components_backward_in_expr(t, _Leaf, 0, 3))

   assert leaves[0] is t.leaves[5]
   assert leaves[1] is t.leaves[4]
   assert leaves[2] is t.leaves[3]
   assert len(leaves) == 3


def test_componenttools_iterate_components_backward_in_expr_10( ):
   '''From backward start index to backward stop index.'''

   t = Staff(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
   macros.diatonicize(t)

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   leaves = list(componenttools.iterate_components_backward_in_expr(t, _Leaf, 1, 5))

   assert leaves[0] is t.leaves[4]
   assert leaves[1] is t.leaves[3]
   assert leaves[2] is t.leaves[2]
   assert leaves[3] is t.leaves[1]
   assert len(leaves) == 4
