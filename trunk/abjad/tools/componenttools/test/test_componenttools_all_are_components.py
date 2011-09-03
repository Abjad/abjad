from abjad import *


def test_componenttools_all_are_components_01():
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_components(notes)


def test_componenttools_all_are_components_02():
    t = Staff("c'8 d'8 e'8 f'8") * 4
    assert componenttools.all_are_components(t)


def test_componenttools_all_are_components_03():
    t = range(4)
    assert not componenttools.all_are_components(t)


def test_componenttools_all_are_components_04():
    t = []
    assert componenttools.all_are_components(t)
