import abjad
import pytest


def test_scoretools_Chord___setattr___01():
    r'''Slots constrain chord attributes.
    '''

    chord = abjad.Chord("<ef' cs' f''>4")

    assert pytest.raises(AttributeError, "chord.foo = 'bar'")
