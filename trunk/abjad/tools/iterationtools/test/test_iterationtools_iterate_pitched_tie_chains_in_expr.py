from abjad import *


def test_iterationtools_iterate_pitched_tie_chains_in_expr_01():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterationtools.iterate_pitched_tie_chains_in_expr(
        staff, reverse=True))

    assert tie_chains[0].music == staff[3:5].music
    assert tie_chains[1].music == staff[:2].music


def test_iterationtools_iterate_pitched_tie_chains_in_expr_02():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterationtools.iterate_pitched_tie_chains_in_expr(
        staff))

    assert tie_chains[0].music == staff[:2].music
    assert tie_chains[1].music == staff[3:5].music
