# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Container_remove_01():
    r'''Containers remove leaves correctly.
    Leaf abjad.detaches from parentage.
    Leaf withdraws from crossing spanners.
    Leaf carries covered spanners forward.
    Leaf returns after removal.
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

    note = voice[1]
    voice.remove(note)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 (
            e'8
            f'8 )
        }
        '''
        )

    "Note is now d'8 [ ]"

    assert format(note) == "d'8 [ ]"

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Container_remove_02():
    r'''Containers remove nested containers correctly.
    abjad.Container abjad.detaches from parentage.
    abjad.Container withdraws from crossing spanners.
    abjad.Container carries covered spanners forward.
    abjad.Container returns after removal.
    '''

    staff = abjad.Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(staff).by_leaf()
    sequential = staff[0]
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

    staff.remove(sequential)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                e'8 [
                f'8 ]
            }
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()

    assert format(sequential) == abjad.String.normalize(
        r'''
        {
            c'8
            d'8
        }
        '''
        )

    assert abjad.inspect(sequential).is_well_formed()


def test_scoretools_Container_remove_03():
    r'''Container remove works on identity and not equality.
    '''

    note = abjad.Note("c'4")
    container = abjad.Container([abjad.Note("c'4")])

    assert pytest.raises(Exception, 'container.remove(note)')
