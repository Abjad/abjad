# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_BendAfter_format_01():
    r'''Bend formats correctly on notes.
    '''

    note = Note("cs'4")
    bend = marktools.BendAfter(8)
    attach(bend, note)
    assert format(note) == "cs'4 - \\bendAfter #'8.0"
    inspect(note).get_mark(marktools.BendAfter).detach()
    assert format(note) == "cs'4"


def test_marktools_BendAfter_format_02():
    r'''Bend formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    bend = marktools.BendAfter(8)
    attach(bend, chord)
    assert format(chord) == "<cs' d' ef'>4 - \\bendAfter #'8.0"
    inspect(chord).get_mark(marktools.BendAfter).detach()
    assert format(chord) == "<cs' d' ef'>4"


def test_marktools_BendAfter_format_03():
    r'''Bend formats correctly on rests.
    '''

    rest = Rest((1, 4))
    bend = marktools.BendAfter(8)
    attach(bend, rest)
    assert format(rest) == "r4 - \\bendAfter #'8.0"
    inspect(rest).get_mark(marktools.BendAfter).detach()
    assert format(rest) == "r4"
