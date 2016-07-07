# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_splice_01():

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])

    result = mutate(voice[-1]).splice(
        [Note("c'8"), Note("d'8"), Note("e'8")],
        grow_spanners=True,
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[-4:]
    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            c'8
            d'8
            e'8 ]
        }
        '''
        )


def test_agenttools_MutationAgent_splice_02():
    r'''Splices leaf after interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])
    result = mutate(voice[1]).splice(
        [Note("dqs'8")],
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            dqs'8
            e'8 ]
        }
        '''
        )

    assert result == voice[1:3]
    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_splice_03():
    r'''Splices tuplet after tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    voice = Voice([tuplet])
    beam = Beam()
    attach(beam, tuplet[:])
    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    result = mutate(voice[-1]).splice(
        [tuplet],
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[:]


def test_agenttools_MutationAgent_splice_04():
    r'''Splices after container with underspanners.
    '''

    voice = Voice(Container("c'8 c'8") * 2)
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    result = mutate(voice[0]).splice(
        [Note("dqs'8")],
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                c'8
            }
            dqs'8
            {
                c'8
                c'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[0:2]


def test_agenttools_MutationAgent_splice_05():
    r'''Extends leaves rightwards after leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])

    result = mutate(voice[-1]).splice(
        [Note("c'8"), Note("d'8"), Note("e'8")],
        grow_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[-4:]


def test_agenttools_MutationAgent_splice_06():
    r'''Extends leaf rightwards after interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])

    result = mutate(voice[1]).splice(
        [Note("dqs'8")],
        grow_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            dqs'8
            e'8 ]
        }
        '''
        )

    assert result == voice[1:3]
    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_splice_07():
    r'''Splices leaves left of leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = mutate(voice[0]).splice(
        notes,
        direction=Left,
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'16 [
            d'16
            e'16
            c'8
            d'8
            e'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[:4]


def test_agenttools_MutationAgent_splice_08():
    r'''Splices leaf left of interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])
    result = mutate(voice[1]).splice(
        [Note("dqf'8")],
        direction=Left,
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            dqf'8
            d'8
            e'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[1:3]


def test_agenttools_MutationAgent_splice_09():
    r'''Splices tuplet left of tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    voice = Voice([tuplet])
    beam = Beam()
    attach(beam, tuplet[:])
    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    result = mutate(voice[0]).splice(
        [tuplet],
        direction=Left,
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[:]


def test_agenttools_MutationAgent_splice_10():
    r'''Splices left of container with underspanners.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    result = mutate(voice[1]).splice(
        [Note("dqs'8")],
        direction=Left,
        grow_spanners=True,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            dqs'8
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert result == voice[1:]
    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_splice_11():
    r'''Extends leaves leftwards of leaf. Do not extend edge spanners.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = mutate(voice[0]).splice(
        notes,
        direction=Left,
        grow_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'16
            d'16
            e'16
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert result == voice[:4]


def test_agenttools_MutationAgent_splice_12():
    r'''Extends leaf leftwards of interior leaf. Does extend interior spanners.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = Beam()
    attach(beam, voice[:])
    result = mutate(voice[1]).splice(
        [Note("dqf'8")],
        direction=Left,
        grow_spanners=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            dqf'8
            d'8
            e'8 ]
        }
        '''
        )

    assert result == voice[1:3]
    assert inspect_(voice).is_well_formed()
