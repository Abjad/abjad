from abjad import *


def test_componenttools_sum_prolated_duration_of_components_01():
    '''Sum of prolated durations of components in list.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert componenttools.sum_prolated_duration_of_components(t.leaves) == Duration(2, 8)
