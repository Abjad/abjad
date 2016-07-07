# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_extend_01():
    r'''Extend spanner to the right.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1][:])

    beam._extend(voice[2][:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_spannertools_Spanner_extend_02():
    r'''Extend spanner to the right.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, voice[1][:])
    beam._extend(leaves[-2:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )
