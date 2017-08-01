# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner__append_left_01():
    r'''Append container to the left.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])

    beam._append_left(voice[0][-1])
    beam._append_left(voice[0][0])

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


def test_spannertools_Spanner__append_left_02():
    r'''Spanner appends one leaf to the right.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = abjad.Beam()
    abjad.attach(beam, voice[1][:])

    beam._append_left(voice[0][-1])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8 [
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
