# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RootedChordClass___init___01():
    r'''Initializes rooted chord-class from empty input.
    '''

    chord_class = tonalanalysistools.RootedChordClass()

    assert repr(chord_class) == 'CMajorTriadInRootPosition'


def test_tonalanalysistools_RootedChordClass___init___02():

    chord_class = tonalanalysistools.RootedChordClass(
        'g', 'dominant', 7, 'root')

    assert repr(chord_class) == 'GDominantSeventhInRootPosition'
    assert len(chord_class) == 4
    assert chord_class.root == abjad.NamedPitchClass('g')
    assert chord_class.bass == abjad.NamedPitchClass('g')


def test_tonalanalysistools_RootedChordClass___init___03():

    chord_class = tonalanalysistools.RootedChordClass(
        'g', 'dominant', 7, 'first')

    assert repr(chord_class) == 'GDominantSeventhInFirstInversion'
    assert len(chord_class) == 4
    assert chord_class.root == abjad.NamedPitchClass('g')
    assert chord_class.bass == abjad.NamedPitchClass('b')
