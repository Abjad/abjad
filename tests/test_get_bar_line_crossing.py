import abjad


def test_get_bar_line_crossing_01():
    """
    Works with partial.
    """

    staff = abjad.Staff("c'8 d'8 e'4 f'8")
    time_signature = abjad.TimeSignature((2, 8), partial=abjad.Duration(1, 8))
    abjad.attach(time_signature, staff[0])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \partial 8
            \time 2/8
            c'8
            d'8
            e'4
            f'8
        }
        """
    )

    assert not abjad.get.bar_line_crossing(staff[0])
    assert not abjad.get.bar_line_crossing(staff[1])
    assert abjad.get.bar_line_crossing(staff[2])
    assert not abjad.get.bar_line_crossing(staff[3])


def test_get_bar_line_crossing_02():
    """
    Works when no explicit time signature is abjad.attached.
    """

    staff = abjad.Staff("c'2 d'1 e'2")

    assert not abjad.get.bar_line_crossing(staff[0])
    assert abjad.get.bar_line_crossing(staff[1])
    assert not abjad.get.bar_line_crossing(staff[2])
