from abjad import *


def test_Spanner___contains___01():

    note = Note("c'4")
    spanner = spannertools.Spanner([Note("c'4")])

    assert not note in spanner
