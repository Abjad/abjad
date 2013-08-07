# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Leaf_written_duration_01():
    r'''Leaf durations can go up to 'maxima...': duration < (16, 1).
    '''

    note = Note(1, 2)

    assert note.lilypond_format == "cs'\\breve"
    note.written_duration = Duration(3)
    assert note.lilypond_format == "cs'\\breve."
    note.written_duration = Duration(4)
    assert note.lilypond_format == "cs'\\longa"
    note.written_duration = Duration(6)
    assert note.lilypond_format == "cs'\\longa."
    note.written_duration = Duration(7)
    assert note.lilypond_format == "cs'\\longa.."
    note.written_duration = Duration(8)
    assert note.lilypond_format == "cs'\\maxima"
    note.written_duration = Duration(12)
    assert note.lilypond_format == "cs'\\maxima."
    note.written_duration = Duration(14)
    assert note.lilypond_format == "cs'\\maxima.."
    note.written_duration = Duration(15)
    assert note.lilypond_format == "cs'\\maxima..."
    assert py.test.raises(AssignabilityError, 'Note(1, 16)')
