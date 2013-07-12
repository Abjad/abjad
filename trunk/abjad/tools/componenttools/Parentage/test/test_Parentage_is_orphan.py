from abjad import *


def test_Parentage_is_orphan_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff.select_parentage().is_orphan
    for note in staff:
        assert not note.select_parentage().is_orphan
