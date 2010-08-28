from abjad import *
import py.test
py.test.skip('fix numbering after update reimplementation.')


def test__Leaf_number_01( ):
   '''Leaves in staff number correctly.'''

   t = Staff(macros.scale(3))
   assert t[0].number == 0
   assert t[1].number == 1
   assert t[2].number == 2


def test__Leaf_number_02( ):
   '''Leaves in measure in staff number correctly.'''

   t = Staff([Measure((3, 8), macros.scale(3))])
   leaves = t.leaves
   assert leaves[0].number == 0
   assert leaves[1].number == 1
   assert leaves[2].number == 2


def test__Leaf_number_03( ):
   '''Leaves in multiple measures in staff number corretly.'''

   t = Staff(Measure((2, 8), macros.scale(2)) * 3)
   leaves = t.leaves
   assert leaves[0].number == 0
   assert leaves[1].number == 1
   assert leaves[2].number == 2
   assert leaves[3].number == 3
   assert leaves[4].number == 4
   assert leaves[5].number == 5


def test__Leaf_number_04( ):
   '''Orphan leaves number correctly.'''

   t = Note(0, (1, 4))
   assert t.number == 0


def test__Leaf_number_05( ):
   '''Leaves number correctly after contents rotation.'''

   t = Staff(macros.scale(4))

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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\te'8\n\tf'8\n\tc'8\n\td'8\n}"

   assert t[0].number == 0
   assert t[1].number == 1
   assert t[2].number == 2
   assert t[3].number == 3
