import pytest

import abjad


def test_Leaf_written_duration_01():
    """
    Leaf durations can go up to 'maxima...': duration < (16, 1).
    """

    note = abjad.Note(1, 2)

    assert abjad.lilypond(note) == "cs'\\breve"
    note.written_duration = abjad.Duration(3)
    assert abjad.lilypond(note) == "cs'\\breve."
    note.written_duration = abjad.Duration(4)
    assert abjad.lilypond(note) == "cs'\\longa"
    note.written_duration = abjad.Duration(6)
    assert abjad.lilypond(note) == "cs'\\longa."
    note.written_duration = abjad.Duration(7)
    assert abjad.lilypond(note) == "cs'\\longa.."
    note.written_duration = abjad.Duration(8)
    assert abjad.lilypond(note) == "cs'\\maxima"
    note.written_duration = abjad.Duration(12)
    assert abjad.lilypond(note) == "cs'\\maxima."
    note.written_duration = abjad.Duration(14)
    assert abjad.lilypond(note) == "cs'\\maxima.."
    note.written_duration = abjad.Duration(15)
    assert abjad.lilypond(note) == "cs'\\maxima..."

    with pytest.raises(abjad.AssignabilityError):
        abjad.Note(1, 16)
