import abjad


def test_Selection_wellformed_01():
    """
    Well-formedness checking runs correctly against leaves.
    """
    note = abjad.Note("c'4")
    assert abjad.wf.wellformed(note)


def test_Selection_wellformed_02():
    """
    Well-formedness checking runs correctly against containers.
    """
    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    assert abjad.wf.wellformed(staff)
