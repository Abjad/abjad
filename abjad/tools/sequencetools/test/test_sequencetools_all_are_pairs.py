# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_all_are_pairs_01():

    assert sequencetools.all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
    assert sequencetools.all_are_pairs([])


def test_sequencetools_all_are_pairs_02():

    assert not sequencetools.all_are_pairs('foo')
    assert not sequencetools.all_are_pairs(1.5)
    assert not sequencetools.all_are_pairs([1, 2])
    assert not sequencetools.all_are_pairs([(1, 2), (3, 4), (5, 6, 7)])
