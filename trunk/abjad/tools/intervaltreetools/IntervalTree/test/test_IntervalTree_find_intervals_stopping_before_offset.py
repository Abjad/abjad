from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_find_intervals_stopping_before_offset_01():
    blocks = _make_test_intervals()
    target_offset = 0
    expected_payloads = ()
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_before_offset_02():
    blocks = _make_test_intervals()
    target_offset = 9
    expected_payloads = ('a',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_before_offset_03():
    blocks = _make_test_intervals()
    target_offset = 14
    expected_payloads = ('a', 'b', 'c', 'd',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_before_offset_04():
    blocks = _make_test_intervals()
    target_offset = 19
    expected_payloads = ('a', 'b', 'c', 'd',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_before_offset_05():
    blocks = _make_test_intervals()
    target_offset = 26
    expected_payloads = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_IntervalTree_find_intervals_stopping_before_offset_06():
    blocks = _make_test_intervals()
    target_offset = 30
    expected_payloads = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j',)
    expected_blocks = tuple(sorted(filter(lambda x: x.keys()[0] in expected_payloads, blocks),
        key = lambda x: x.signature))
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = IntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_before_offset(target_offset)
        assert expected_blocks == actual_blocks
