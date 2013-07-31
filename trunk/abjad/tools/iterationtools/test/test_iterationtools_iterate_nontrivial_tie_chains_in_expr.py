# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_nontrivial_tie_chains_in_expr_01():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    tie_chains = list(iterationtools.iterate_nontrivial_tie_chains_in_expr(staff, reverse=True))

    assert tie_chains[0].leaves == staff.select_leaves()[-2:]
    assert tie_chains[1].leaves == staff.select_leaves()[:2]


def test_iterationtools_iterate_nontrivial_tie_chains_in_expr_02():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    tie_chains = list(iterationtools.iterate_nontrivial_tie_chains_in_expr(staff))

    assert tie_chains[0].leaves == staff.select_leaves()[:2]
    assert tie_chains[1].leaves == staff.select_leaves()[-2:]
