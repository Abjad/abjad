import abjad


def test_Staff_time_signature_01():
    """
    Force time signature on nonempty staff.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff[0])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        """
    )


def test_Staff_time_signature_02():
    """
    Staff time signature carries over to staff-contained leaves.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff[0])
    for x in staff:
        assert abjad.inspect(x).effective(
            abjad.TimeSignature
        ) == abjad.TimeSignature((2, 4))


def test_Staff_time_signature_03():
    """
    Staff time signature set and then clear.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff[0])
    abjad.detach(time_signature, staff[0])
    for leaf in staff:
        assert abjad.inspect(leaf).effective(abjad.TimeSignature) is None
