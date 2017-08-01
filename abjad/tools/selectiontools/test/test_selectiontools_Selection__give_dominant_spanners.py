# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Selection__give_dominant_spanners_01():
    r'''Find spanners that dominate donor_components.
    Apply dominant spanners to recipient_components.
    Withdraw donor_components from spanners.
    The operation can mangle spanners.
    Remove donor_components from parentage immediately after.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, voice[:])
    beam = abjad.Beam()
    abjad.attach(beam, voice[:2])
    slur = abjad.Slur()
    abjad.attach(slur, voice[1:3])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \<
            d'8 ] (
            e'8 )
            f'8 \!
        }
        '''
        )

    recipient = abjad.Voice("c'16 c'16 c'16")
    beam = abjad.Beam()
    abjad.attach(beam, recipient[:])

    assert format(recipient) == abjad.String.normalize(
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

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \<
            d'8 ]
            e'8
            f'8 \!
        }
        '''
        )

    assert not abjad.inspect(voice).is_well_formed()

    "Slur is contiguous but recipient participates in discont. cresc."

    assert format(recipient) == abjad.String.normalize(
        r'''
        \new Voice {
            c'16 [ (
            c'16
            c'16 ] )
        }
        '''
        )

    assert not abjad.inspect(recipient).is_well_formed()
