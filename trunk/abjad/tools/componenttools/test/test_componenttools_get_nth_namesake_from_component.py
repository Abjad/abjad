from abjad import *
import py.test


def test_componenttools_get_nth_namesake_from_component_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert componenttools.get_nth_namesake_from_component(t[0], 0) is t[0]
    assert componenttools.get_nth_namesake_from_component(t[0], 1) is t[1]
    assert componenttools.get_nth_namesake_from_component(t[0], 2) is t[2]
    assert componenttools.get_nth_namesake_from_component(t[0], 3) is t[3]

    assert componenttools.get_nth_namesake_from_component(t[3], 0) is t[3]
    assert componenttools.get_nth_namesake_from_component(t[3], -1) is t[2]
    assert componenttools.get_nth_namesake_from_component(t[3], -2) is t[1]
    assert componenttools.get_nth_namesake_from_component(t[3], -3) is t[0]


def test_componenttools_get_nth_namesake_from_component_02():

    t = Staff("c'8 d'8 e'8 f'8")

    assert py.test.raises(IndexError, 'componenttools.get_nth_namesake_from_component(t[0], 99)')
