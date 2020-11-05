import abjad


def test_Parentage__id_string_01():
    """
    Returns component name if it exists. Otherwise Python ID.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    parentage = abjad.get.parentage(staff)
    assert parentage._id_string(staff).startswith("Staff-")


def test_Parentage__id_string_02():
    """
    Returns component name if it exists. Otherwise Python ID.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    parentage = abjad.get.parentage(staff)
    staff.name = "foo"
    assert parentage._id_string(staff) == "Staff-'foo'"
