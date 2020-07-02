import abjad


def test_Mutation__move_indicators_01():

    staff = abjad.Staff(r'\clef "bass" c \staccato d e f')

    assert format(staff) == abjad.String.normalize(
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

    assert len(abjad.inspect(staff[0]).indicators()) == 2
    assert len(abjad.inspect(staff[1]).indicators()) == 0
    assert len(abjad.inspect(staff[2]).indicators()) == 0
    assert len(abjad.inspect(staff[3]).indicators()) == 0

    abjad.Mutation._move_indicators(staff[0], staff[2])

    assert format(staff) == abjad.String.normalize(
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

    assert len(abjad.inspect(staff[0]).indicators()) == 0
    assert len(abjad.inspect(staff[1]).indicators()) == 0
    assert len(abjad.inspect(staff[2]).indicators()) == 2
    assert len(abjad.inspect(staff[3]).indicators()) == 0
