# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
import pytest


def test_sequencetools_divide_sequence_elements_by_greatest_common_divisor_01():
    r'''Divide sequence elements by greatest common divisor.
    '''

    result = sequencetools.divide_sequence_elements_by_greatest_common_divisor([2, 2, -4, -16])
    assert result == [1, 1, -2, -8]

    result = sequencetools.divide_sequence_elements_by_greatest_common_divisor([-1, -1, 4, 16])
    assert result == [-1, -1, 4, 16]

    result = sequencetools.divide_sequence_elements_by_greatest_common_divisor([2, 2, 4, 17])
    assert result == [2, 2, 4, 17]


def test_sequencetools_divide_sequence_elements_by_greatest_common_divisor_02():
    r'''Raise exception on noninteger input.
    '''

    assert pytest.raises(TypeError,
        'sequencetools.divide_sequence_elements_by_greatest_common_divisor([2, 2, 3.5])')


def test_sequencetools_divide_sequence_elements_by_greatest_common_divisor_03():
    r'''Raises exception when zero in input.
    '''

    assert pytest.raises(NotImplementedError,
        'sequencetools.divide_sequence_elements_by_greatest_common_divisor([0, 2, 2])')
