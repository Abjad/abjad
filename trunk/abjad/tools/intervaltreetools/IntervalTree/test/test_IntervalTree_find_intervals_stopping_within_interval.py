from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools import BoundedInterval
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_find_intervals_stopping_within_interval_01():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(-10, 0)
    expected_payloads = ()
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_02():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(0, 9)
    expected_payloads = ('a', 'd',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_03():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(4, 19)
    expected_payloads = ('b', 'c', 'd', 'g',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_04():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(6, 10)
    expected_payloads = ('c', 'd',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_05():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(13, 15)
    expected_payloads = ('b',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_06():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(14, 25)
    expected_payloads = ('e', 'f', 'g', 'h',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_07():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(19, 26)
    expected_payloads = ('e', 'f', 'g', 'h',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_08():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(24, 31)
    expected_payloads = ('i', 'j',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_09():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(26, 29)
    expected_payloads = ('j',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_within_interval_10():
    blocks = _make_test_intervals()
    target_interval = BoundedInterval(30, 40)
    expected_payloads = ('i', 'k', 'l',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks
