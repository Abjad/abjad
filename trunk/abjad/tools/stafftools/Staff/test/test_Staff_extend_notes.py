# -*- encoding: utf-8 -*-
from abjad import *


def test_Staff_extend_notes_01():
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[0:1]))
    assert select(staff).is_well_formed()


def test_Staff_extend_notes_02():
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[0:3]))
    assert select(staff).is_well_formed()


def test_Staff_extend_notes_03():
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[1:7]))
    assert select(staff).is_well_formed()


def test_Staff_extend_notes_04():
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[5:7]))
    assert select(staff).is_well_formed()
