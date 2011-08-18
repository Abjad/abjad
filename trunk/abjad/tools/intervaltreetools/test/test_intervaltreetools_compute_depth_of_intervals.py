from abjad.tools.intervaltreetools import compute_depth_of_intervals
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_compute_depth_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    depths = compute_depth_of_intervals(tree)
    target = [
        ((0, 3), 1),
        ((3, 5), 0),
        ((5, 6), 1),
        ((6, 8), 2),
        ((8, 9), 3),
        ((9, 10), 2),
        ((10, 13), 1),
        ((13, 15), 0),
        ((15, 16), 1),
        ((16, 17), 2),
        ((17, 19), 3),
        ((19, 20), 3),
        ((20, 21), 2),
        ((21, 23), 1),
        ((23, 25), 0),
        ((25, 26), 1),
        ((26, 29), 2),
        ((29, 30), 1),
        ((30, 32), 0),
        ((32, 34), 1),
        ((34, 37), 1),
    ]
    actual = [(i.signature, i['depth']) for i in depths]
    assert actual == target
