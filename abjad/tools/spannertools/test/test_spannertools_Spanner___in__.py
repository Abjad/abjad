# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___in___01():
    r'''Spanner containment tests components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert voice[1] in beam
    assert voice[1][0] not in beam
    assert voice[1][1] not in beam


def test_spannertools_Spanner___in___02():
    r'''Spanner containment tests components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
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
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert all(x in beam for x in (voice[0], voice[1], voice[2]))
    assert not any(x in beam for x in voice.select_leaves())
