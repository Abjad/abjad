import pytest

import abjad


def test_Leaf_duration_assign_01():
    """
    Written duration can be assigned a duration.
    """

    note = abjad.Note("cs'4")
    note.set_written_duration(abjad.ValueDuration(1, 8))
    assert note.written_duration() == abjad.ValueDuration(1, 8)


def test_Leaf_duration_compare_01():
    """
    Written durations can be evaluated for equality with durations.
    """

    note = abjad.Note("c'4")
    assert note.written_duration() == abjad.ValueDuration(1, 4)


def test_Leaf_duration_compare_02():
    """
    Written durations can be evaluated for equality with integers.
    """

    note = abjad.Note("c'1")
    assert note.written_duration() == abjad.ValueDuration(1)


def test_Leaf_duration_compare_03():
    """
    Written durations can NOT be evaluated for equality with tuples.
    """

    note = abjad.Note("c'4")
    assert note.written_duration() == abjad.ValueDuration(1, 4)
    assert note.written_duration() != (1, 4)
    assert note.written_duration() != "foo"


def test_Leaf_written_duration_01():
    """
    Leaf durations can go up to 'maxima...': duration < (16, 1).
    """

    note = abjad.Note(r"cs'\breve")

    assert abjad.lilypond(note) == "cs'\\breve"
    note.set_written_duration(abjad.ValueDuration(3))
    assert abjad.lilypond(note) == "cs'\\breve."
    note.set_written_duration(abjad.ValueDuration(4))
    assert abjad.lilypond(note) == "cs'\\longa"
    note.set_written_duration(abjad.ValueDuration(6))
    assert abjad.lilypond(note) == "cs'\\longa."
    note.set_written_duration(abjad.ValueDuration(7))
    assert abjad.lilypond(note) == "cs'\\longa.."
    note.set_written_duration(abjad.ValueDuration(8))
    assert abjad.lilypond(note) == "cs'\\maxima"
    note.set_written_duration(abjad.ValueDuration(12))
    assert abjad.lilypond(note) == "cs'\\maxima."
    note.set_written_duration(abjad.ValueDuration(14))
    assert abjad.lilypond(note) == "cs'\\maxima.."
    note.set_written_duration(abjad.ValueDuration(15))
    assert abjad.lilypond(note) == "cs'\\maxima..."

    with pytest.raises(abjad.AssignabilityError):
        duration = abjad.ValueDuration(16)
        pitch = abjad.NamedPitch("cs")
        abjad.Note.from_duration_and_pitch(duration, pitch)
