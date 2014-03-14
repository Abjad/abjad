# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_Sequence_reverse_01():
    r'''Reverse sequence.
    '''

    assert sequencetools.Sequence(1, 2, 3, 4, 5).reverse() == \
        sequencetools.Sequence(5, 4, 3, 2, 1)
    assert sequencetools.Sequence(1, 2, 3, 4, 5).reverse() == \
        sequencetools.Sequence(5, 4, 3, 2, 1)
