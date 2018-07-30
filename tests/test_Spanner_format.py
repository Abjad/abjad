import abjad


def test_Spanner_format_01():
    """
    Base Spanner class makes no format-time contributions.
    However, base spanner causes no explosions at format-time, either.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    spanner = abjad.Spanner()
    abjad.attach(spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )

    assert abjad.inspect(staff).is_wellformed()
