from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_01():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(-10, 0)
    expected_payloads = ('a',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_02():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(0, 9)
    expected_payloads = ('a', 'b', 'c', 'd',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_03():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(4, 19)
    expected_payloads = ('b', 'c', 'd', 'e', 'f', 'g', 'h',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_04():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(6, 10)
    expected_payloads = ('b', 'c', 'd',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_05():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(13, 15)
    expected_payloads = ('b', 'e',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_06():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(14, 25)
    expected_payloads = ('e', 'f', 'g', 'h', 'i',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_07():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(19, 26)
    expected_payloads = ('e', 'f', 'g', 'h', 'i', 'j',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_08():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(24, 31)
    expected_payloads = ('i', 'j',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_09():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(26, 29)
    expected_payloads = ('i', 'j',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_intersecting_or_tangent_to_interval_10():
    blocks = _make_test_intervals()
    target_interval = TimeInterval(30, 40)
    expected_payloads = ('i', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_intersecting_or_tangent_to_interval(target_interval)
        assert expected_blocks == actual_blocks
