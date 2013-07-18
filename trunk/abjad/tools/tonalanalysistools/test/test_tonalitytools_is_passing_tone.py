from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalitytools_is_passing_tone_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert not tonalanalysistools.is_passing_tone(t[0])
    assert tonalanalysistools.is_passing_tone(t[1])
    assert tonalanalysistools.is_passing_tone(t[2])
    assert not tonalanalysistools.is_passing_tone(t[3])
