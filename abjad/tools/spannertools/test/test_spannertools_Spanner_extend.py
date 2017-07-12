# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner_extend_01():
    r'''Extend spanner to the right.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])

    beam._extend(voice[2][:])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_spannertools_Spanner_extend_02():
    r'''Extend spanner to the right.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])
    beam._extend(leaves[-2:])

    assert format(voice) == abjad.String.normalize(
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
