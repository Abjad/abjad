import abjad


def test_Staff___init___01():
    """
    Initialize with context name.
    """

    staff = abjad.Staff(lilypond_type='BlueStaff')
    assert staff.lilypond_type == 'BlueStaff'


def test_Staff___init___02():
    """
    Initialize with name.
    """

    staff = abjad.Staff(name='FirstBlueStaff')
    assert staff.name == 'FirstBlueStaff'


def test_Staff___init___03():
    """
    Initialize with both context name and name.
    """

    staff = abjad.Staff(lilypond_type='BlueStaff', name='FirstBlueStaff')
    assert staff.lilypond_type == 'BlueStaff'
    assert staff.name == 'FirstBlueStaff'
