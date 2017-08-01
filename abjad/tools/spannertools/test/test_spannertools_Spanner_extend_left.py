# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner_extend_left_01():
    r'''Extend spanner to the left.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[2:4])
    beam._extend_left(leaves[:2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()
