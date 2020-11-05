import pytest

import abjad


def test_get_duration_01():
    """
    Container duration in seconds equals sum of leaf durations in seconds.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=38
                c'8
                d'8
                \tempo 4=42
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.get.duration(score, in_seconds=True) == abjad.Duration(400, 133)


def test_get_duration_02():
    """
    Container can not calculate duration in seconds without metronome mark.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")
    with pytest.raises(Exception):
        abjad.get.duration(container, in_seconds=True)


def test_get_duration_03():
    """
    Clock duration equals duration divide by effective tempo.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])
    abjad.Score([staff])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tempo 4=38
            c'8
            d'8
            \tempo 4=42
            e'8
            f'8
        }
        """
    )

    assert abjad.get.duration(staff[0], in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.get.duration(staff[1], in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.get.duration(staff[2], in_seconds=True) == abjad.Duration(5, 7)
    assert abjad.get.duration(staff[3], in_seconds=True) == abjad.Duration(5, 7)


def test_get_duration_04():
    """
    Clock duration can not calculate without metronome mark.
    """

    note = abjad.Note("c'4")
    with pytest.raises(Exception):
        abjad.get.duration(note, in_seconds=True)
