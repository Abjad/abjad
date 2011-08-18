from abjad import *


def test_componenttools_all_are_components_scalable_by_multiplier_01():
    t = [Note(0, (1, 8))]
    assert componenttools.all_are_components_scalable_by_multiplier(t, Duration(1, 2))


def test_componenttools_all_are_components_scalable_by_multiplier_02():
    t = [Note(0, (1, 8))]
    assert componenttools.all_are_components_scalable_by_multiplier(t, Duration(2, 1))


def test_componenttools_all_are_components_scalable_by_multiplier_03():
    t = [Note(0, (1, 8))]
    assert not componenttools.all_are_components_scalable_by_multiplier(t, Duration(2, 3))


def test_componenttools_all_are_components_scalable_by_multiplier_04():
    t = [Note(0, (1, 8))]
    assert componenttools.all_are_components_scalable_by_multiplier(t, Duration(3, 2))


def test_componenttools_all_are_components_scalable_by_multiplier_05():
    t = [Note(0, (3, 16))]
    assert componenttools.all_are_components_scalable_by_multiplier(t, Duration(2, 3))


def test_componenttools_all_are_components_scalable_by_multiplier_06():
    t = [Note(0, (3, 16))]
    assert not componenttools.all_are_components_scalable_by_multiplier(t, Duration(3, 2))
