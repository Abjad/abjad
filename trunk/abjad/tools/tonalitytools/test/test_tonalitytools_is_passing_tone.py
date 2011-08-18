from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_is_passing_tone_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert not tonalitytools.is_passing_tone(t[0])
    assert tonalitytools.is_passing_tone(t[1])
    assert tonalitytools.is_passing_tone(t[2])
    assert not tonalitytools.is_passing_tone(t[3])
