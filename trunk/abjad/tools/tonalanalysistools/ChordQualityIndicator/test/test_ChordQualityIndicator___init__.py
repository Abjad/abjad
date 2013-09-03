# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ChordQualityIndicator___init___01():
    r'''Init root position triad.
    '''

    cqi = tonalanalysistools.ChordQualityIndicator('major', 'triad')
    assert str(cqi) == '<P1, +M3, +P5>'

    cqi = tonalanalysistools.ChordQualityIndicator('minor', 'triad')
    assert str(cqi) == '<P1, +m3, +P5>'

    cqi = tonalanalysistools.ChordQualityIndicator('diminished', 'triad')
    assert str(cqi) == '<P1, +m3, +dim5>'

    cqi = tonalanalysistools.ChordQualityIndicator('augmented', 'triad')
    assert str(cqi) == '<P1, +M3, +aug5>'


def test_ChordQualityIndicator___init___02():
    r'''Init seventh and ninth.
    '''

    cqi = tonalanalysistools.ChordQualityIndicator('dominant', 7, 'root')
    assert str(cqi) == '<P1, +M3, +P5, +m7>'

    cqi = tonalanalysistools.ChordQualityIndicator('dominant', 9, 'root')
    assert str(cqi) == '<P1, +M3, +P5, +m7, +M9>'


def test_ChordQualityIndicator___init___03():
    r'''Init with quality string and integer cardinality indicator.
    '''

    cqi = tonalanalysistools.ChordQualityIndicator('dominant', 7)
    assert str(cqi) == '<P1, +M3, +P5, +m7>'

    cqi = tonalanalysistools.ChordQualityIndicator('major', 7)
    assert str(cqi) == '<P1, +M3, +P5, +M7>'

    cqi = tonalanalysistools.ChordQualityIndicator('diminished', 7)
    assert str(cqi) == '<P1, +m3, +dim5, +dim7>'

    cqi = tonalanalysistools.ChordQualityIndicator('dominant', 9)
    assert str(cqi) == '<P1, +M3, +P5, +m7, +M9>'
