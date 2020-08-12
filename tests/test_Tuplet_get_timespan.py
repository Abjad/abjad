import abjad


def test_Tuplet_get_timespan_01():

    staff = abjad.Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")
    leaves = abjad.select(staff).leaves()
    score = abjad.Score([staff])
    mark = abjad.MetronomeMark((1, 4), 60)
    abjad.attach(mark, leaves[0])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=60
                c'4
                d'4
                \times 2/3 {
                    e'4
                    f'4
                    g'4
                }
            }
        >>
        """
    )

    assert abjad.get.timespan(staff, in_seconds=True) == abjad.Timespan(0, 4)
    assert abjad.get.timespan(staff[0], in_seconds=True) == abjad.Timespan(0, 1)
    assert abjad.get.timespan(staff[1], in_seconds=True) == abjad.Timespan(1, 2)
    assert abjad.get.timespan(staff[-1], in_seconds=True) == abjad.Timespan(2, 4)
