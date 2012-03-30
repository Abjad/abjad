from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree_find_intervals_stopping_after_offset_01():
    blocks = _make_test_intervals()
    target_offset = 0
    expected_payloads = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_stopping_after_offset_02():
    blocks = _make_test_intervals()
    target_offset = 9
    expected_payloads = ('b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_stopping_after_offset_03():
    blocks = _make_test_intervals()
    target_offset = 14
    expected_payloads = ('e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_stopping_after_offset_04():
    blocks = _make_test_intervals()
    target_offset = 19
    expected_payloads = ('e', 'f', 'h', 'i', 'j', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_stopping_after_offset_05():
    blocks = _make_test_intervals()
    target_offset = 26
    expected_payloads = ('i', 'j', 'k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks

def test_TimeIntervalTree_find_intervals_stopping_after_offset_06():
    blocks = _make_test_intervals()
    target_offset = 30
    expected_payloads = ('k', 'l')
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_stopping_after_offset(target_offset)
        assert expected_blocks == actual_blocks
