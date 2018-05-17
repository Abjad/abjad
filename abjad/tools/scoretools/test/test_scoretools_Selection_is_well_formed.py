import abjad


def test_scoretools_Selection_is_well_formed_01():
    """
    Well-formedness checking runs correctly against leaves.
    """
    note = abjad.Note("c'4")
    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Selection_is_well_formed_02():
    """
    Well-formedness checking runs correctly against containers.
    """
    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    assert abjad.inspect(staff).is_well_formed()
