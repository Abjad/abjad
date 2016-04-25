# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_TwelveToneRow___init___01():
    r'''Rows initialize with nonnegative integers.
    '''

    numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
    row = pitchtools.TwelveToneRow(numbers)


def test_pitchtools_TwelveToneRow___init___02():
    r'''Rows initialize with pitch-classes.
    '''

    numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
    pitch_classes = [pitchtools.NumberedPitchClass(number) for number in numbers]
    row = pitchtools.TwelveToneRow(pitch_classes)


def test_pitchtools_TwelveToneRow___init___03():
    r'''Rows initialize from other rows.
    '''

    numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
    row = pitchtools.TwelveToneRow(numbers)
    new = pitchtools.TwelveToneRow(row)


def test_pitchtools_TwelveToneRow___init___04():
    r'''Rows do not initialize with defective pitch-class content.
    '''

    assert pytest.raises(ValueError, 'pitchtools.TwelveToneRow([0, 1, 2, 3])')
