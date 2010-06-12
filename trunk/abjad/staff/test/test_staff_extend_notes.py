from abjad import *


def test_staff_extend_notes_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[0 : 1]))
   assert check.wf(t)


def test_staff_extend_notes_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[0 : 3]))
   assert check.wf(t)


def test_staff_extend_notes_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[1 : 7]))
   assert check.wf(t)


def test_staff_extend_notes_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[5 : 7]))
   assert check.wf(t)
