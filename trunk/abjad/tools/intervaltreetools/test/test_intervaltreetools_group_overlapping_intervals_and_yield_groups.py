from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_group_overlapping_intervals_and_yield_groups_01():
    tree = IntervalTree(_make_test_intervals())

    target_signatures = [
        [(0, 3)],
        [(5, 13), (6, 10), (8, 9)],
        [(15, 23), (16, 21), (17, 19), (19, 20)],
        [(25, 30), (26, 29)],
        [(32, 34)],
        [(34, 37)],
    ]

    actual_signatures = []
    for group in group_overlapping_intervals_and_yield_groups(tree):
        signature_group = []
        for interval in group:
            signature_group.append(interval.signature)
        actual_signatures.append(signature_group)

    assert actual_signatures == target_signatures
