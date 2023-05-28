import pytest

import abjad


def test_Leaf_duration_assign_01():
    """
    Written duration can be assigned a duration.
    """

    note = abjad.Note(1, (1, 4))
    note.written_duration = abjad.Duration(1, 8)
    assert note.written_duration == abjad.Duration(1, 8)


def test_Leaf_duration_assign_02():
    """
    Written duration can be assigned an integer.
    """

    note = abjad.Note(1, (1, 4))
    note.written_duration = 2
    assert note.written_duration == abjad.Duration(2, 1)


def test_Leaf_duration_assign_03():
    """
    Written duration can be assigned an tuple.
    """

    note = abjad.Note(1, (1, 4))
    note.written_duration = (1, 2)
    assert note.written_duration == abjad.Duration(1, 2)


def test_Leaf_duration_compare_01():
    """
    Written durations can be evaluated for equality with durations.
    """

    note = abjad.Note("c'4")
    assert note.written_duration == abjad.Duration(1, 4)


def test_Leaf_duration_compare_02():
    """
    Written durations can be evaluated for equality with integers.
    """

    note = abjad.Note(0, 1)
    assert note.written_duration == 1


def test_Leaf_duration_compare_03():
    """
    Written durations can NOT be evaluated for equality with tuples.
    """

    note = abjad.Note("c'4")
    assert note.written_duration == abjad.Duration(1, 4)
    assert note.written_duration != (1, 4)
    assert note.written_duration != "foo"


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
