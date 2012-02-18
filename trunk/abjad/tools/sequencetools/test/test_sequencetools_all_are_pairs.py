from abjad.tools.sequencetools import all_are_pairs


def test_sequencetools_all_are_pairs_01():
    assert all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
    assert all_are_pairs([])


def test_sequencetools_all_are_pairs_02():
    assert not all_are_pairs('foo')
    assert not all_are_pairs(1.5)
    assert not all_are_pairs([1, 2])
    assert not all_are_pairs([(1, 2), (3, 4), (5, 6, 7)])
