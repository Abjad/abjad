import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_group_overlapping_intervals_and_yield_groups_01( ):
    tree = IntervalTree(_make_test_blocks( ))

    target_signatures = [ 
        [(0, 3)],
        [(5, 13), (6, 10), (8, 9)],
        [(15, 23), (16, 21), (17, 19), (19, 20)],
        [(25, 30), (26, 29)],
        [(32, 34)],
        [(34, 37)],
    ]

    actual_signatures = [ ]
    for group in group_overlapping_intervals_and_yield_groups(tree):
        signature_group = [ ]
        for interval in group:
            signature_group.append(interval.signature)
        actual_signatures.append(signature_group)

    assert actual_signatures == target_signatures


