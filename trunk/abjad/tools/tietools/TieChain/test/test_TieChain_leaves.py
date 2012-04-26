from abjad import *


def test_TieChain_leaves_01():

    staff = Staff("c' ~ c'16")

    assert tietools.get_tie_chain(staff[0]).leaves == tuple(staff[:])


def test_TieChain_leaves_02():

    staff = Staff("c'")

    assert tietools.get_tie_chain(staff[0]).leaves == (staff[0], )
