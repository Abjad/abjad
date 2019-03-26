import abjad
import pytest


def test_Chord___setattr___01():
    """
    Slots constrain chord attributes.
    """

    chord = abjad.Chord("<ef' cs' f''>4")

    with pytest.raises(AttributeError):
        chord.foo = 'bar'
