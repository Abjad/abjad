from abjad import *


def test_TieChain_leaves_01():

    staff = Staff("c' ~ c'16")

    assert staff[0].get_tie_chain().leaves == tuple(staff[:])


def test_TieChain_leaves_02():

    staff = Staff("c'")

    assert staff[0].get_tie_chain().leaves == (staff[0], )
