# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Chord___setattr___01():
    r'''Slots constrain chord attributes.
    '''

    chord = Chord("<ef' cs' f''>4")

    assert pytest.raises(AttributeError, "chord.foo = 'bar'")
