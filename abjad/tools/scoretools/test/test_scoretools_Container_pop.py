# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Container_pop_01():
    r'''Containers pop leaves correctly.
    Popped leaves abjad.detach from parent.
    Popped leaves withdraw from crossing spanners.
    Popped leaves carry covered spanners forward.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    slur = abjad.Slur()
    abjad.attach(slur, voice[:])
    beam = abjad.Beam()
    abjad.attach(beam, voice[1])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 (
            d'8 [ ]
            e'8
            f'8 )
        }
        '''
        )

    result = voice.pop(1)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 (
            e'8
            f'8 )
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()

    "Result is now d'8 [ ]"

    assert abjad.inspect(result).is_well_formed()
    assert format(result) == "d'8 [ ]"


def test_scoretools_Container_pop_02():
    r'''Containers pop nested containers correctly.
    Popped containers abjad.detach from both parent and spanners.
    '''

    staff = abjad.Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
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

    sequential = staff.pop()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                c'8 [
                d'8 ]
            }
        }
        '''
        )
    assert abjad.inspect(staff).is_well_formed()

    assert format(sequential) == abjad.String.normalize(
        r'''
        {
            e'8
            f'8
        }
        '''
        )

    assert abjad.inspect(sequential).is_well_formed()
