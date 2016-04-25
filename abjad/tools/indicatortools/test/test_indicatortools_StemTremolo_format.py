# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_StemTremolo_format_01():
    r'''Tremolo formats correctly on notes.
    '''

    note = Note("cs'4")
    stem_tremolo = indicatortools.StemTremolo(8)
    attach(stem_tremolo, note)
    assert format(note) == "cs'4 :8"
    detach(stem_tremolo, note)
    assert format(note) == "cs'4"


def test_indicatortools_StemTremolo_format_02():
    r'''Tremolo formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    stem_tremolo = indicatortools.StemTremolo(8)
    attach(stem_tremolo, chord)
    assert format(chord) == "<cs' d' ef'>4 :8"
    detach(stem_tremolo, chord)
    assert format(chord) == "<cs' d' ef'>4"


def test_indicatortools_StemTremolo_format_03():
    r'''Tremolo formats correctly on rests.
    '''

    rest = Rest((1, 4))
    stem_tremolo = indicatortools.StemTremolo(8)
    attach(stem_tremolo, rest)
    assert format(rest) == "r4 :8"
    detach(stem_tremolo, rest)
    assert format(rest) == "r4"
