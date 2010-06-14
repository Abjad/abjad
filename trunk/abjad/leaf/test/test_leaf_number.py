from abjad import *


def test_leaf_number_01( ):
   '''Leaves in staff number correctly.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   assert t[0].number == 0
   assert t[1].number == 1
   assert t[2].number == 2


def test_leaf_number_02( ):
   '''Leaves in measure in staff number correctly.'''

   t = Staff([RigidMeasure((3, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))])
   leaves = t.leaves
   assert leaves[0].number == 0
   assert leaves[1].number == 1
   assert leaves[2].number == 2


def test_leaf_number_03( ):
   '''Leaves in multiple measures in staff number corretly.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)) * 3)
   leaves = t.leaves
   assert leaves[0].number == 0
   assert leaves[1].number == 1
   assert leaves[2].number == 2
   assert leaves[3].number == 3
   assert leaves[4].number == 4
   assert leaves[5].number == 5


def test_leaf_number_04( ):
   '''Orphan leaves number correctly.'''

   t = Note(0, (1, 4))
   assert t.number == 0


def test_leaf_number_05( ):
   '''Leaves number correctly after contents rotation.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))

   assert t[0].number == 0
   assert t[1].number == 1
   assert t[2].number == 2
   assert t[3].number == 3

   t[:] = (t[-2:] + t[:2])

   r'''
   \new Staff {
      e'8
      f'8
      c'8
      d'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\te'8\n\tf'8\n\tc'8\n\td'8\n}"

   assert t[0].number == 0
   assert t[1].number == 1
   assert t[2].number == 2
   assert t[3].number == 3
