import pytest

import abjad


def test_bind_01():
    """
    REGRESSION. Make sure no exceptions are raised when updating
    wrappers that have been orphaned because a context was removed.
    In this example, the metronome mark finds the score context at
    attachment time. After the score is removed, the metronome mark
    must properly update its effective context to none.
    """

    voice = abjad.Voice("c'4")
    staff = abjad.Staff([voice])
    score = abjad.Score([staff])
    leaf = abjad.select.leaf(staff, 0)
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 72)
    abjad.attach(mark, leaf)
    score[:] = []
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                \tempo 4=72
                c'4
            }
        }
        """
    )


def test_bind_02():
    """
    Make sure exception is raised when check_duplicate_indicator=True.
    """

    score = abjad.Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    mark_1 = abjad.MetronomeMark(abjad.Duration(1, 8), 52)
    mark_2 = abjad.MetronomeMark(abjad.Duration(1, 8), 73)
    abjad.attach(mark_1, score[0][0])

    with pytest.raises(Exception):
        abjad.attach(mark_2, score[1][0], check_duplicate_indicator=True)
