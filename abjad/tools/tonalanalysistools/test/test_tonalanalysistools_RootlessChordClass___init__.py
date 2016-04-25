# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RootlessChordClass___init___01():
    r'''Initialize root position triad.
    '''

    cqi = tonalanalysistools.RootlessChordClass('major', 'triad')
    assert str(cqi) == '<P1, +M3, +P5>'

    cqi = tonalanalysistools.RootlessChordClass('minor', 'triad')
    assert str(cqi) == '<P1, +m3, +P5>'

    cqi = tonalanalysistools.RootlessChordClass('diminished', 'triad')
    assert str(cqi) == '<P1, +m3, +dim5>'

    cqi = tonalanalysistools.RootlessChordClass('augmented', 'triad')
    assert str(cqi) == '<P1, +M3, +aug5>'


def test_tonalanalysistools_RootlessChordClass___init___02():
    r'''Initialize seventh and ninth.
    '''

    cqi = tonalanalysistools.RootlessChordClass('dominant', 7, 'root')
    assert str(cqi) == '<P1, +M3, +P5, +m7>'

    cqi = tonalanalysistools.RootlessChordClass('dominant', 9, 'root')
    assert str(cqi) == '<P1, +M3, +P5, +m7, +M9>'


def test_tonalanalysistools_RootlessChordClass___init___03():
    r'''Initialize with quality string and integer cardinality.
    '''

    cqi = tonalanalysistools.RootlessChordClass('dominant', 7)
    assert str(cqi) == '<P1, +M3, +P5, +m7>'

    cqi = tonalanalysistools.RootlessChordClass('major', 7)
    assert str(cqi) == '<P1, +M3, +P5, +M7>'

    cqi = tonalanalysistools.RootlessChordClass('diminished', 7)
    assert str(cqi) == '<P1, +m3, +dim5, +dim7>'

    cqi = tonalanalysistools.RootlessChordClass('dominant', 9)
    assert str(cqi) == '<P1, +M3, +P5, +m7, +M9>'
