from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_permute_sequence_01():
    '''Permute list.
    '''

    assert sequencetools.permute_sequence([11, 12, 13, 14], [1, 0, 3, 2]) == [12, 11, 14, 13]


def test_sequencetools_permute_sequence_02():
    '''Permute tuple.
    '''

    assert sequencetools.permute_sequence((11, 12, 13, 14), [1, 0, 3, 2]) == (12, 11, 14, 13)


def test_sequencetools_permute_sequence_03():
    '''Permute Abjad container.
    '''

    container = Container("c'8 d'8 e'8")
    assert sequencetools.permute_sequence(container, [2, 0, 1]).format == Container("e'8 c'8 d'8").format


def test_sequencetools_permute_sequence_04():
    '''Permute string.
    '''

    assert sequencetools.permute_sequence('heart', [4, 0, 1, 2, 3]) == 'thear'
