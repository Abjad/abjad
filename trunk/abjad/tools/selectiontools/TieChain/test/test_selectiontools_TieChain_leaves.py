# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_TieChain_leaves_01():

    staff = Staff("c' ~ c'16")

    assert inspect(staff[0]).get_tie_chain().leaves == tuple(staff[:])


def test_selectiontools_TieChain_leaves_02():

    staff = Staff("c'")

    assert inspect(staff[0]).get_tie_chain().leaves == (staff[0], )
