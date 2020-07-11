import abjad


def test_Inspection_bar_line_crossing_01():
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

    assert not abjad.inspect(staff[0]).bar_line_crossing()
    assert not abjad.inspect(staff[1]).bar_line_crossing()
    assert abjad.inspect(staff[2]).bar_line_crossing()
    assert not abjad.inspect(staff[3]).bar_line_crossing()


def test_Inspection_bar_line_crossing_02():
    """
    Works when no explicit time signature is abjad.attached.
    """

    staff = abjad.Staff("c'2 d'1 e'2")

    assert not abjad.inspect(staff[0]).bar_line_crossing()
    assert abjad.inspect(staff[1]).bar_line_crossing()
    assert not abjad.inspect(staff[2]).bar_line_crossing()
