# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Chord___setattr___01():
    r'''Slots constrain chord attributes.
    '''

    chord = Chord("<ef' cs' f''>4")

    assert pytest.raises(AttributeError, "chord.foo = 'bar'")
