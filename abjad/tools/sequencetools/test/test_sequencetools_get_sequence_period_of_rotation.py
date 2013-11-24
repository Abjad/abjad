# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_get_sequence_period_of_rotation_01():

    assert sequencetools.get_sequence_period_of_rotation([1, 1, 1, 1, 1, 1], 1) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 2, 1, 2], 1) == 2
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 2, 1], 1) == 3
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 1, 1], 1) == 6


def test_sequencetools_get_sequence_period_of_rotation_02():

    assert sequencetools.get_sequence_period_of_rotation([1, 1, 1, 1, 1, 1], 2) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 2, 1, 2], 2) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 2, 1], 2) == 3
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 1, 1], 2) == 3


def test_sequencetools_get_sequence_period_of_rotation_03():

    assert sequencetools.get_sequence_period_of_rotation([1, 1, 1, 1, 1, 1], 3) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 2, 1, 2], 3) == 2
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 2, 1], 3) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 1, 1], 3) == 2


def test_sequencetools_get_sequence_period_of_rotation_04():

    assert sequencetools.get_sequence_period_of_rotation([1, 1, 1, 1, 1, 1], 10) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 2, 1, 2], 10) == 1
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 2, 1], 10) == 3
    assert sequencetools.get_sequence_period_of_rotation([1, 2, 1, 1, 1, 1], 10) == 3


def test_sequencetools_get_sequence_period_of_rotation_05():
    r'''Empty iterable boundary case.
    '''

    statement = 'sequencetools.get_sequence_period_of_rotation([], 1)'
    assert pytest.raises(ZeroDivisionError, statement)
