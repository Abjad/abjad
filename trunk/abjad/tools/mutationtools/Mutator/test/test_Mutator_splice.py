# -*- encoding: utf-8 -*-
from abjad import *


def test_Mutator_splice_01():

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])

    result = mutate(voice[-1]).splice(
        [Note("c'8"), Note("d'8"), Note("e'8")], 
        grow_spanners=True,
        )

    assert select(voice).is_well_formed()
    assert result == voice[-4:]
    assert testtools.compare(
        voice,
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


def test_Mutator_splice_02():
    r'''Splice leaf after interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    result = mutate(voice[1]).splice(
        [Note(2.5, (1, 8))], 
        grow_spanners=True,
        )

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
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


def test_Mutator_splice_03():
    r'''Splice tuplet after tuplet.
    '''

    voice = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(voice[0])
    result = mutate(voice[-1]).splice(
        [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], 
        grow_spanners=True,
        )

    assert select(voice).is_well_formed()
    assert result == voice[:]
    assert testtools.compare(
        voice,
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


def test_Mutator_splice_04():
    r'''Splice after container with underspanners.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    spannertools.BeamSpanner(voice.select_leaves())
    result = mutate(voice[0]).splice(
        [Note(2.5, (1, 8))], 
        grow_spanners=True,
        )

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    assert result == voice[0:2]


def test_Mutator_splice_05():
    r'''Extend leaves rightwards after leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])

    result = mutate(voice[-1]).splice(
        [Note("c'8"), Note("d'8"), Note("e'8")], 
        grow_spanners=False,
        )

    assert testtools.compare(
        voice,
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

    assert select(voice).is_well_formed()
    assert result == voice[-4:]


def test_Mutator_splice_06():
    r'''Extend leaf rightwards after interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])

    result = mutate(voice[1]).splice(
        [Note(2.5, (1, 8))], 
        grow_spanners=False,
        )

    assert testtools.compare(
        voice,
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
    assert select(voice).is_well_formed()


def test_Mutator_splice_07():
    r'''Splice leaves left of leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = mutate(voice[0]).splice(
        notes, 
        direction=Left, 
        grow_spanners=True,
        )

    assert testtools.compare(
        voice,
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

    assert select(voice).is_well_formed()
    assert result == voice[:4]


def test_Mutator_splice_08():
    r'''Splice leaf left of interior leaf.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    result = mutate(voice[1]).splice(
        [Note(1.5, (1, 8))], 
        direction=Left, 
        grow_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            dqf'8
            d'8
            e'8 ]
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert result == voice[1:3]


def test_Mutator_splice_09():
    r'''Splice tuplet left of tuplet.
    '''

    voice = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(voice[0])
    result = mutate(voice[0]).splice(
        [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], 
        direction=Left,
        grow_spanners=True,
        )

    assert testtools.compare(
        voice,
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

    assert select(voice).is_well_formed()
    assert result == voice[:]


def test_Mutator_splice_10():
    r'''Splice left of container with underspanners.
    '''

    voice = Voice(2 * Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())
    result = mutate(voice[1]).splice(
        [Note(2.5, (1, 8))], 
        direction=Left,
        grow_spanners=True,
        )

    assert testtools.compare(
        voice,
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
    assert select(voice).is_well_formed()


def test_Mutator_splice_11():
    r'''Extend leaves leftwards of leaf. Do not extend edge spanners.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = mutate(voice[0]).splice(
        notes,
        direction=Left,
        grow_spanners=False,
        )

    assert testtools.compare(
        voice,
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

    assert select(voice).is_well_formed()
    assert result == voice[:4]


def test_Mutator_splice_12():
    r'''Extend leaf leftwards of interior leaf. Do extend interior spanners.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    result = mutate(voice[1]).splice(
        [Note(1.5, (1, 8))], 
        direction=Left,
        grow_spanners=False,
        )

    assert testtools.compare(
        voice,
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
    assert select(voice).is_well_formed()
