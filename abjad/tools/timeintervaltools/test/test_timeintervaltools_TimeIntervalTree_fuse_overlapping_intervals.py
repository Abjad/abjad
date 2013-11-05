# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_timeintervaltools_TimeIntervalTree_fuse_overlapping_intervals_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    fused_tree = tree.fuse_overlapping_intervals()
    target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in fused_tree]
    assert target_signatures == actual_signatures
    assert tree.duration == fused_tree.duration


def test_timeintervaltools_TimeIntervalTree_fuse_overlapping_intervals_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    fused_tree = tree.fuse_overlapping_intervals(
        include_tangent_intervals=True)
    target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 37)]
    actual_signatures = [interval.signature for interval in fused_tree]
    assert target_signatures == actual_signatures
    assert tree.duration == fused_tree.duration
