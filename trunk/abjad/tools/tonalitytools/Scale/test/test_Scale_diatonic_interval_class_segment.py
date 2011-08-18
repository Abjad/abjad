from abjad import *
from abjad.tools import tonalitytools


def test_Scale_diatonic_interval_class_segment_01():

    scale = tonalitytools.Scale('a', 'major')
    dicg = scale.diatonic_interval_class_segment

    assert str(dicg) == '<M2, M2, m2, M2, M2, M2, m2>'


def test_Scale_diatonic_interval_class_segment_02():

    scale = tonalitytools.Scale('a', 'dorian')
    dicg = scale.diatonic_interval_class_segment

    assert str(dicg) == '<M2, m2, M2, M2, M2, m2, M2>'
