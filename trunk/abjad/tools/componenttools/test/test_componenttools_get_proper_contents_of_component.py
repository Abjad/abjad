from abjad import *


def test_componenttools_get_proper_contents_of_component_01():

    staff = Staff("c' d' e' f'")

    assert componenttools.get_proper_contents_of_component(staff) == staff[:]


def test_componenttools_get_proper_contents_of_component_02():

    note = Note("c'4")

    assert componenttools.get_proper_contents_of_component(note) == []
