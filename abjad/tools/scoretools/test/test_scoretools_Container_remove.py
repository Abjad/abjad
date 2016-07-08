# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Container_remove_01():
    r'''Containers remove leaves correctly.
    Leaf detaches from parentage.
    Leaf withdraws from crossing spanners.
    Leaf carries covered spanners forward.
    Leaf returns after removal.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, voice[:])
    beam = Beam()
    attach(beam, voice[1])

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()
    assert inspect_(note).is_well_formed()


def test_scoretools_Container_remove_02():
    r'''Containers remove nested containers correctly.
    Container detaches from parentage.
    Container withdraws from crossing spanners.
    Container carries covered spanners forward.
    Container returns after removal.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    leaves = select(staff).by_leaf()
    sequential = staff[0]
    beam = Beam()
    attach(beam, leaves)

    assert format(staff) == stringtools.normalize(
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

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                e'8 [
                f'8 ]
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()

    assert format(sequential) == stringtools.normalize(
        r'''
        {
            c'8
            d'8
        }
        '''
        )

    assert inspect_(sequential).is_well_formed()


def test_scoretools_Container_remove_03():
    r'''Container remove works on identity and not equality.
    '''

    note = Note("c'4")
    container = Container([Note("c'4")])

    assert pytest.raises(Exception, 'container.remove(note)')
