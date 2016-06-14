# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_extend_left_01():
    r'''Extend spanner to the left.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1][:])
    beam._extend_left(voice[0][:])

    assert format(voice) == stringtools.normalize(
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
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_spannertools_Spanner_extend_left_02():
    r'''Extend spanner to the left.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1][:])
    beam._extend_left(voice[0:1][:])

    assert format(voice) == stringtools.normalize(
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
            {
                g'8
                a'8
            }
        }
        '''
        )