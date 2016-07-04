# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection__give_dominant_spanners_01():
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

    assert format(voice) == stringtools.normalize(
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

    assert format(recipient) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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

    assert format(recipient) == stringtools.normalize(
        r'''
        \new Voice {
            c'16 [ (
            c'16
            c'16 ] )
        }
        '''
        )

    assert not inspect_(recipient).is_well_formed()