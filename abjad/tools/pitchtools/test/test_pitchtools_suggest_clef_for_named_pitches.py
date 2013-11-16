# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_suggest_clef_for_named_pitches_01():

    pitches = [10, 20, 30]
    pitches = [NamedPitch(x) for x in pitches]

    assert pitchtools.suggest_clef_for_named_pitches(pitches) == Clef('treble')


def test_pitchtools_suggest_clef_for_named_pitches_02():

    pitches = [-10, -20, -30]
    pitches = [NamedPitch(x) for x in pitches]

    assert pitchtools.suggest_clef_for_named_pitches(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_for_named_pitches_03():

    pitches = [10, 20, -30]
    pitches = [NamedPitch(x) for x in pitches]

    assert pitchtools.suggest_clef_for_named_pitches(pitches) == Clef('bass')


def test_pitchtools_suggest_clef_for_named_pitches_04():

    pitches = [-10, -20, 30]
    pitches = [NamedPitch(x) for x in pitches]

    assert pitchtools.suggest_clef_for_named_pitches(pitches) == Clef('treble')


def test_pitchtools_suggest_clef_for_named_pitches_05():
    r'''Works with arbitrary expression.
    '''

    staff = Staff(scoretools.make_notes(range(-12, -6), [(1, 4)]))

    assert pitchtools.suggest_clef_for_named_pitches(staff) == Clef('bass')
