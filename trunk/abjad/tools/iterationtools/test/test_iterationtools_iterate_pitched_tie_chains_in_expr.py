# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_pitched_tie_chains_in_expr_01():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterationtools.iterate_pitched_tie_chains_in_expr(
        staff, reverse=True))

    assert tie_chains[0] == selectiontools.TieChain(staff[3:5])
    assert tie_chains[1] == selectiontools.TieChain(staff[:2])


def test_iterationtools_iterate_pitched_tie_chains_in_expr_02():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterationtools.iterate_pitched_tie_chains_in_expr(
        staff))

    assert tie_chains[0] == selectiontools.TieChain(staff[:2])
    assert tie_chains[1] == selectiontools.TieChain(staff[3:5])
