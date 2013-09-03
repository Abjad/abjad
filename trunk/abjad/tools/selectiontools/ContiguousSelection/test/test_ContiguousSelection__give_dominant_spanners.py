# -*- encoding: utf-8 -*-
from abjad import *


def test_SliceSelection__give_dominant_spanners_01():
    r'''Find spanners that dominate donor_components.
    Apply dominant spanners to recipient_components.
    Withdraw donor_components from spanners.
    The operation can mangle spanners.
    Remove donor_components from parentage immediately after.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.CrescendoSpanner(voice[:])
    spannertools.BeamSpanner(voice[:2])
    spannertools.SlurSpanner(voice[1:3])

    r'''
    \new Voice {
        c'8 [ \<
        d'8 ] (
        e'8 )
        f'8 \!
    }
    '''

    recipient = Voice(notetools.make_repeated_notes(3, Duration(1, 16)))
    spannertools.BeamSpanner(recipient[:])

    r'''
    \new Voice {
        c'16 [
        c'16
        c'16 ]
    }
    '''

    voice[1:3]._give_dominant_spanners(recipient[:])

    "Voice voice is now ..."

    r'''
    \new Voice {
        c'8 [ \<
        d'8 ]
        e'8
        f'8 \!
    }
    '''

    "Both crescendo and beam are now discontiguous."

    assert not inspect(voice).is_well_formed()
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

    "Recipient is now ..."

    r'''
    \new Voice {
        c'16 [ (
        c'16
        c'16 ] )
    }
    '''

    "Slur is contiguous but recipient participates in discont. cresc."

    assert not inspect(recipient).is_well_formed()
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


def test_SliceSelection__give_dominant_spanners_02():
    r'''Not composer-safe.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice[:])

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

    donor = voice[0]
    recipient = Voice("c'8 d'8 e'8 f'8")
    voice[:1]._give_dominant_spanners([recipient])

    "Container voice is now ..."

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

    "Recipient container is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8
    }
    '''

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

    "Both container voice and recipient container carry discontiguous spanners."

    assert not inspect(voice).is_well_formed()
    assert not inspect(recipient).is_well_formed()
