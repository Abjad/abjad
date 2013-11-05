# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_ContiguousSelection__give_dominant_spanners_01():
    r'''Find spanners that dominate donor_components.
    Apply dominant spanners to recipient_components.
    Withdraw donor_components from spanners.
    The operation can mangle spanners.
    Remove donor_components from parentage immediately after.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    crescendo = spannertools.CrescendoSpanner()
    attach(crescendo, voice[:])
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:2])
    slur = spannertools.SlurSpanner()
    attach(slur, voice[1:3])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \<
            d'8 ] (
            e'8 )
            f'8 \!
        }
        '''
        )

    recipient = Voice(scoretools.make_repeated_notes(3, Duration(1, 16)))
    beam = spannertools.BeamSpanner()
    attach(beam, recipient[:])

    assert testtools.compare(
        recipient,
        r'''
        \new Voice {
            c'16 [
            c'16
            c'16 ]
        }
        '''
        )

    voice[1:3]._give_dominant_spanners(recipient[:])


    "Both crescendo and beam are now discontiguous."

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \<
            d'8 ]
            e'8
            f'8 \!
        }
        '''
        )

    assert not inspect(voice).is_well_formed()

    "Slur is contiguous but recipient participates in discont. cresc."

    assert testtools.compare(
        recipient,
        r'''
        \new Voice {
            c'16 [ (
            c'16
            c'16 ] )
        }
        '''
        )

    assert not inspect(recipient).is_well_formed()


def test_selectiontools_ContiguousSelection__give_dominant_spanners_02():
    r'''Not composer-safe.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    donor = voice[0]
    recipient = Voice("c'8 d'8 e'8 f'8")
    voice[:1]._give_dominant_spanners([recipient])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        recipient,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8
        }
        '''
        )

    "Both voice and recipient container carry discontiguous spanners."

    assert not inspect(voice).is_well_formed()
    assert not inspect(recipient).is_well_formed()
