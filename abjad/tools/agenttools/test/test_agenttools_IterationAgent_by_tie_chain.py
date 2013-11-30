# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_logical_tie_01():
    r'''Yield successive logical ties.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))
    tie = spannertools.Tie()
    attach(tie, staff[:2])
    tie = spannertools.Tie()
    attach(tie, staff[2:])

    assert systemtools.TestManager.compare(
        staff,
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
    r'''Yield successive logical ties.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))

    logical_ties = list(iterate(staff).by_logical_tie(reverse=True))

    assert logical_ties[0] == selectiontools.LogicalTie(staff[3])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[2])
    assert logical_ties[2] == selectiontools.LogicalTie(staff[1])
    assert logical_ties[3] == selectiontools.LogicalTie(staff[0])


def test_agenttools_IterationAgent_by_logical_tie_03():
    r'''Yield successive logical ties.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))
    tie = spannertools.Tie()
    attach(tie, staff[:2])
    tie = spannertools.Tie()
    attach(tie, staff[2:])

    logical_ties = list(iterate(staff).by_logical_tie())

    assert logical_ties[0] == selectiontools.LogicalTie((staff[0], staff[1]))
    assert logical_ties[1] == selectiontools.LogicalTie((staff[2], staff[3]))


def test_agenttools_IterationAgent_by_logical_tie_04():
    r'''Yield successive logical ties.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))

    r'''
    \new Staff {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    logical_ties = list(iterate(staff).by_logical_tie())

    assert logical_ties[0] == selectiontools.LogicalTie(staff[0])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[1])
    assert logical_ties[2] == selectiontools.LogicalTie(staff[2])
    assert logical_ties[3] == selectiontools.LogicalTie(staff[3])


def test_agenttools_IterationAgent_by_logical_tie_05():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    logical_ties = list(iterate(staff).by_logical_tie(
        nontrivial=True, reverse=True))

    assert logical_ties[0].leaves == staff.select_leaves()[-2:]
    assert logical_ties[1].leaves == staff.select_leaves()[:2]


def test_agenttools_IterationAgent_by_logical_tie_06():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    logical_ties = list(iterate(staff).by_logical_tie(nontrivial=True))

    assert logical_ties[0].leaves == staff.select_leaves()[:2]
    assert logical_ties[1].leaves == staff.select_leaves()[-2:]


def test_agenttools_IterationAgent_by_logical_tie_07():

    staff = Staff('c ~ c r d ~ d r')

    logical_ties = list(iterate(staff).by_logical_tie(
        pitched=True, reverse=True))

    assert logical_ties[0] == selectiontools.LogicalTie(staff[3:5])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[:2])


def test_agenttools_IterationAgent_by_logical_tie_08():

    staff = Staff('c ~ c r d ~ d r')

    logical_ties = list(iterate(staff).by_logical_tie(pitched=True))

    assert logical_ties[0] == selectiontools.LogicalTie(staff[:2])
    assert logical_ties[1] == selectiontools.LogicalTie(staff[3:5])
