import abjad


def test_Staff_append_01():
    """
    Append one note.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 4)
    staff.append(abjad.Note("c'4"))
    assert abjad.inspect(staff).is_wellformed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)


def test_Staff_append_02():
    """
    Append one chord.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 4)
    staff.append(abjad.Chord([2, 3, 4], (1, 4)))
    assert abjad.inspect(staff).is_wellformed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)


def test_Staff_append_03():
    """
    Append one tuplet.
    """

    staff = abjad.Staff(abjad.Note("c'4") * 4)
    staff.append(abjad.Tuplet((2, 3), 3 * abjad.Note(0, (1, 8))))
    assert abjad.inspect(staff).is_wellformed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == abjad.Duration(5, 4)
