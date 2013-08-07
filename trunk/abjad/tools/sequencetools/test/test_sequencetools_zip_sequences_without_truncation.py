# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_zip_sequences_without_truncation_01():
    r'''Zip and do not truncate to the length of the shortest list.
    '''

    sequence_2 = sequencetools.zip_sequences_without_truncation([1, 2, 3, 4], [11, 12, 13])
    assert sequence_2 == [(1, 11), (2, 12), (3, 13), (4,)]


def test_sequencetools_zip_sequences_without_truncation_02():
    r'''Zip and do not truncate to the length of the shortest list.
    '''

    sequence_2 = sequencetools.zip_sequences_without_truncation([1, 2, 3], [11, 12, 13, 14])
    assert sequence_2 == [(1, 11), (2, 12), (3, 13), (14,)]
