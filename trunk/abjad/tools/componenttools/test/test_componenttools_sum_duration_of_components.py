from abjad import *


def test_componenttools_sum_duration_of_components_01():
    '''Sum of prolated durations of components in list.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert componenttools.sum_duration_of_components(t.leaves) == Duration(2, 8)


def test_componenttools_sum_duration_of_components_02():
    '''Return sum of preprolated duration of components in list.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert componenttools.sum_duration_of_components(t[:], preprolated=True) == Duration(3, 8)


def test_componenttools_sum_duration_of_components_03():
    '''Return zero for empty list.
    '''

    assert componenttools.sum_duration_of_components([], preprolated=True) == Duration(0)
