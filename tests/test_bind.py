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
