# -*- encoding: utf-8 -*-
from abjad import *


def test_TieChain_leaves_01():

    staff = Staff("c' ~ c'16")

    assert more(staff[0]).select_tie_chain().leaves == tuple(staff[:])


def test_TieChain_leaves_02():

    staff = Staff("c'")

    assert more(staff[0]).select_tie_chain().leaves == (staff[0], )
