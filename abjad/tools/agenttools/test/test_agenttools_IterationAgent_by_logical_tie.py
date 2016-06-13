# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_logical_tie_01():
    r'''Yields successive logical ties.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    tie = Tie()
    attach(tie, staff[:2])
    tie = Tie()
    attach(tie, staff[2:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 ~
            c'8
            c'8 ~
            c'8
        }
        '''
        )

    logical_ties = list(iterate(staff).by_logical_tie(reverse=True))

    assert logical_ties[0] == selectiontools.LogicalTie((staff[2], staff[3]))
    assert logical_ties[1] == selectiontools.LogicalTie((staff[0], staff[1]))


def test_agenttools_IterationAgent_by_logical_tie_02():
    r'''Yields successive logical ties.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")

    logical_ties = list(iterate(staff).by_logical_tie(reverse=True))

    assert logical_ties[0] == selectiontools.LogicalTie(staff[3])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[2])
    assert logical_ties[2] == selectiontools.LogicalTie(staff[1])
    assert logical_ties[3] == selectiontools.LogicalTie(staff[0])


def test_agenttools_IterationAgent_by_logical_tie_03():
    r'''Yields successive logical ties.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    tie = Tie()
    attach(tie, staff[:2])
    tie = Tie()
    attach(tie, staff[2:])

    logical_ties = list(iterate(staff).by_logical_tie())

    assert logical_ties[0] == selectiontools.LogicalTie((staff[0], staff[1]))
    assert logical_ties[1] == selectiontools.LogicalTie((staff[2], staff[3]))


def test_agenttools_IterationAgent_by_logical_tie_04():
    r'''Yields successive logical ties.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    logical_ties = list(iterate(staff).by_logical_tie())

    assert logical_ties[0] == selectiontools.LogicalTie(staff[0])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[1])
    assert logical_ties[2] == selectiontools.LogicalTie(staff[2])
    assert logical_ties[3] == selectiontools.LogicalTie(staff[3])


def test_agenttools_IterationAgent_by_logical_tie_05():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
    leaves = list(iterate(staff).by_leaf())

    logical_ties = iterate(staff).by_logical_tie(nontrivial=True, reverse=True)
    logical_ties = list(logical_ties)

    assert logical_ties[0].leaves == tuple(leaves[-2:])
    assert logical_ties[1].leaves == tuple(leaves[:2])


def test_agenttools_IterationAgent_by_logical_tie_06():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
    leaves = list(iterate(staff).by_leaf())

    logical_ties = list(iterate(staff).by_logical_tie(nontrivial=True))

    assert logical_ties[0].leaves == tuple(leaves[:2])
    assert logical_ties[1].leaves == tuple(leaves[-2:])


def test_agenttools_IterationAgent_by_logical_tie_07():

    staff = Staff('c ~ c r d ~ d r')

    logical_ties = iterate(staff).by_logical_tie(pitched=True, reverse=True)
    logical_ties = list(logical_ties)

    assert logical_ties[0] == selectiontools.LogicalTie(staff[3:5])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[:2])


def test_agenttools_IterationAgent_by_logical_tie_08():

    staff = Staff('c ~ c r d ~ d r')

    logical_ties = list(iterate(staff).by_logical_tie(pitched=True))

    assert logical_ties[0] == selectiontools.LogicalTie(staff[:2])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[3:5])


def test_agenttools_IterationAgent_by_logical_tie_09():

    staff = Staff("{ c'4 d'4 ~ } { d'4 e'4 ~ } { e'4 f'4 }")

    logical_ties = list(iterate(staff[1]).by_logical_tie())

    assert len(logical_ties) == 2
    assert len(logical_ties[0]) == 2
    assert len(logical_ties[1]) == 2
    assert logical_ties[0][0] is staff[0][1]
    assert logical_ties[0][1] is staff[1][0]
    assert logical_ties[1][0] is staff[1][1]
    assert logical_ties[1][1] is staff[2][0]


def test_agenttools_IterationAgent_by_logical_tie_10():

    staff = Staff("{ c'4 d'4 ~ } { d'4 e'4 ~ } { e'4 f'4 }")

    logical_ties = list(iterate(staff[1])
        .by_logical_tie(parentage_mask=staff[1])
        )

    assert len(logical_ties) == 2
    assert len(logical_ties[0]) == 1
    assert len(logical_ties[1]) == 1
    assert logical_ties[0][0] is staff[1][0]
    assert logical_ties[1][0] is staff[1][1]


def test_agenttools_IterationAgent_by_logical_tie_11():
    r'''No logical ties, but no errors either.'''
    staff = Staff()
    logical_ties = list(iterate(staff).by_logical_tie())
    assert len(logical_ties) == 0
