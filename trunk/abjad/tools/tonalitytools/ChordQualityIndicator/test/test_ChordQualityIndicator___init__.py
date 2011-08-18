from abjad import *
from abjad.tools import tonalitytools


def test_ChordQualityIndicator___init___01():
    '''Init root position triad.'''

    cqi = tonalitytools.ChordQualityIndicator('major', 'triad')
    assert str(cqi) == '<P1, M3, P5>'

    cqi = tonalitytools.ChordQualityIndicator('minor', 'triad')
    assert str(cqi) == '<P1, m3, P5>'

    cqi = tonalitytools.ChordQualityIndicator('diminished', 'triad')
    assert str(cqi) == '<P1, m3, dim5>'

    cqi = tonalitytools.ChordQualityIndicator('augmented', 'triad')
    assert str(cqi) == '<P1, M3, aug5>'


def test_ChordQualityIndicator___init___02():
    '''Init seventh and ninth.'''

    cqi = tonalitytools.ChordQualityIndicator('dominant', 7, 'root')
    assert str(cqi) == '<P1, M3, P5, m7>'

    cqi = tonalitytools.ChordQualityIndicator('dominant', 9, 'root')
    assert str(cqi) == '<P1, M3, P5, m7, M9>'


def test_ChordQualityIndicator___init___03():
    '''Init with quality string and integer cardinality indicator.'''

    cqi = tonalitytools.ChordQualityIndicator('dominant', 7)
    assert str(cqi) == '<P1, M3, P5, m7>'

    cqi = tonalitytools.ChordQualityIndicator('major', 7)
    assert str(cqi) == '<P1, M3, P5, M7>'

    cqi = tonalitytools.ChordQualityIndicator('diminished', 7)
    assert str(cqi) == '<P1, m3, dim5, dim7>'

    cqi = tonalitytools.ChordQualityIndicator('dominant', 9)
    assert str(cqi) == '<P1, M3, P5, m7, M9>'
