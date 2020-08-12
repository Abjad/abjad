import abjad


def test_mutate__move_indicators_01():

    staff = abjad.Staff(r'\clef "bass" c \staccato d e f')

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "bass"
            c4
            - \staccato
            d4
            e4
            f4
        }
        """
    )

    assert len(abjad.get.indicators(staff[0])) == 2
    assert len(abjad.get.indicators(staff[1])) == 0
    assert len(abjad.get.indicators(staff[2])) == 0
    assert len(abjad.get.indicators(staff[3])) == 0

    abjad.mutate._move_indicators(staff[0], staff[2])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c4
            d4
            \clef "bass"
            e4
            - \staccato
            f4
        }
        """
    )

    assert len(abjad.get.indicators(staff[0])) == 0
    assert len(abjad.get.indicators(staff[1])) == 0
    assert len(abjad.get.indicators(staff[2])) == 2
    assert len(abjad.get.indicators(staff[3])) == 0
