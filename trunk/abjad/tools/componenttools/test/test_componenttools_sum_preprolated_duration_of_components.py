from abjad import *
import py.test


def test_componenttools_sum_preprolated_duration_of_components_01():
    '''Return sum of preprolated duration of components in list.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert componenttools.sum_preprolated_duration_of_components(t[:]) == Duration(3, 8)


def test_componenttools_sum_preprolated_duration_of_components_02():
    '''Return zero for empty list.'''

    assert componenttools.sum_preprolated_duration_of_components([]) == Duration(0)
