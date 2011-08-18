from abjad import *


def test_Staff_extend_notes_01():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[0:1]))
    assert componenttools.is_well_formed_component(t)


def test_Staff_extend_notes_02():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[0:3]))
    assert componenttools.is_well_formed_component(t)


def test_Staff_extend_notes_03():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[1:7]))
    assert componenttools.is_well_formed_component(t)


def test_Staff_extend_notes_04():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[5:7]))
    assert componenttools.is_well_formed_component(t)
