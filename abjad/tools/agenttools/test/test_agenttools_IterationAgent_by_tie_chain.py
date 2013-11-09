# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_tie_chain_01():
    r'''Yield successive tie chains.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))
    tie = spannertools.Tie()
    attach(tie, staff[:2])
    tie = spannertools.Tie()
    attach(tie, staff[2:])

    assert testtools.compare(
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

    chains = list(iterate(staff).by_tie_chain(reverse=True))

    assert chains[0] == selectiontools.TieChain((staff[2], staff[3]))
    assert chains[1] == selectiontools.TieChain((staff[0], staff[1]))


def test_agenttools_IterationAgent_by_tie_chain_02():
    r'''Yield successive tie chains.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))

    chains = list(iterate(staff).by_tie_chain(reverse=True))

    assert chains[0] == selectiontools.TieChain(staff[3])
    assert chains[1] == selectiontools.TieChain(staff[2])
    assert chains[2] == selectiontools.TieChain(staff[1])
    assert chains[3] == selectiontools.TieChain(staff[0])


def test_agenttools_IterationAgent_by_tie_chain_03():
    r'''Yield successive tie chains.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))
    tie = spannertools.Tie()
    attach(tie, staff[:2])
    tie = spannertools.Tie()
    attach(tie, staff[2:])

    chains = list(iterate(staff).by_tie_chain())

    assert chains[0] == selectiontools.TieChain((staff[0], staff[1]))
    assert chains[1] == selectiontools.TieChain((staff[2], staff[3]))


def test_agenttools_IterationAgent_by_tie_chain_04():
    r'''Yield successive tie chains.
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

    chains = list(iterate(staff).by_tie_chain())

    assert chains[0] == selectiontools.TieChain(staff[0])
    assert chains[1] == selectiontools.TieChain(staff[1])
    assert chains[2] == selectiontools.TieChain(staff[2])
    assert chains[3] == selectiontools.TieChain(staff[3])


def test_agenttools_IterationAgent_by_tie_chain_05():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    tie_chains = list(iterate(staff).by_tie_chain(
        nontrivial=True, reverse=True))

    assert tie_chains[0].leaves == staff.select_leaves()[-2:]
    assert tie_chains[1].leaves == staff.select_leaves()[:2]


def test_agenttools_IterationAgent_by_tie_chain_06():

    staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    tie_chains = list(iterate(staff).by_tie_chain(nontrivial=True))

    assert tie_chains[0].leaves == staff.select_leaves()[:2]
    assert tie_chains[1].leaves == staff.select_leaves()[-2:]


def test_agenttools_IterationAgent_by_tie_chain_07():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterate(staff).by_tie_chain(
        pitched=True, reverse=True))

    assert tie_chains[0] == selectiontools.TieChain(staff[3:5])
    assert tie_chains[1] == selectiontools.TieChain(staff[:2])


def test_agenttools_IterationAgent_by_tie_chain_08():

    staff = Staff('c ~ c r d ~ d r')

    tie_chains = list(iterate(staff).by_tie_chain(pitched=True))

    assert tie_chains[0] == selectiontools.TieChain(staff[:2])
    assert tie_chains[1] == selectiontools.TieChain(staff[3:5])
