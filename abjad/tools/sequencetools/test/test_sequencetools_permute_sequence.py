# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_permute_sequence_01():
    r'''Permute list.
    '''

    assert sequencetools.permute_sequence([11, 12, 13, 14], [1, 0, 3, 2]) == [12, 11, 14, 13]


def test_sequencetools_permute_sequence_02():
    r'''Permute tuple.
    '''

    assert sequencetools.permute_sequence((11, 12, 13, 14), [1, 0, 3, 2]) == (12, 11, 14, 13)


def test_sequencetools_permute_sequence_03():
    r'''Permute string.
    '''

    assert sequencetools.permute_sequence('heart', [4, 0, 1, 2, 3]) == 'thear'
