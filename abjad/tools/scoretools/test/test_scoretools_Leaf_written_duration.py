import abjad
import pytest


def test_scoretools_Leaf_written_duration_01():
    r'''Leaf durations can go up to 'maxima...': duration < (16, 1).
    '''

    note = abjad.Note(1, 2)

    assert format(note) == "cs'\\breve"
    note.written_duration = abjad.Duration(3)
    assert format(note) == "cs'\\breve."
    note.written_duration = abjad.Duration(4)
    assert format(note) == "cs'\\longa"
    note.written_duration = abjad.Duration(6)
    assert format(note) == "cs'\\longa."
    note.written_duration = abjad.Duration(7)
    assert format(note) == "cs'\\longa.."
    note.written_duration = abjad.Duration(8)
    assert format(note) == "cs'\\maxima"
    note.written_duration = abjad.Duration(12)
    assert format(note) == "cs'\\maxima."
    note.written_duration = abjad.Duration(14)
    assert format(note) == "cs'\\maxima.."
    note.written_duration = abjad.Duration(15)
    assert format(note) == "cs'\\maxima..."
    assert pytest.raises(abjad.AssignabilityError, 'abjad.Note(1, 16)')
