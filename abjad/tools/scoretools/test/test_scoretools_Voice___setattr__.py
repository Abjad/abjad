import abjad
import pytest


def test_scoretools_Voice___setattr___01():
    r'''Slots constrain voice attributes.
    '''

    voice = abjad.Voice([])

    assert pytest.raises(AttributeError, "voice.foo = 'bar'")
