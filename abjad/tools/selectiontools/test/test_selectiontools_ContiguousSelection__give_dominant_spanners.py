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
    crescendo = Crescendo()
    attach(crescendo, voice[:])
    beam = Beam()
    attach(beam, voice[:2])
    slur = Slur()
    attach(slur, voice[1:3])

    assert systemtools.TestManager.compare(
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

    recipient = Voice("c'16 c'16 c'16")
    beam = Beam()
    attach(beam, recipient[:])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert not inspect_(voice).is_well_formed()

    "Slur is contiguous but recipient participates in discont. cresc."

    assert systemtools.TestManager.compare(
        recipient,
        r'''
        \new Voice {
            c'16 [ (
            c'16
            c'16 ] )
        }
        '''
        )

    assert not inspect_(recipient).is_well_formed()


def test_selectiontools_ContiguousSelection__give_dominant_spanners_02():
    r'''Not composer-safe.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice[:])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert not inspect_(voice).is_well_formed()
    assert not inspect_(recipient).is_well_formed()