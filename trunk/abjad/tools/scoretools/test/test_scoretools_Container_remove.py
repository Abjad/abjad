# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_Container_remove_01():
    r'''Containers remove leaves correctly.
    Leaf detaches from parentage.
    Leaf withdraws from crossing spanners.
    Leaf carries covered spanners forward.
    Leaf returns after removal.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner()
    attach(slur, voice[:])
    beam = spannertools.BeamSpanner()
    attach(beam, voice[1])

    assert testtools.compare(
        voice,
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

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 (
            e'8
            f'8 )
        }
        '''
        )

    "Note is now d'8 [ ]"

    assert note.lilypond_format == "d'8 [ ]"

    assert inspect(voice).is_well_formed()
    assert inspect(note).is_well_formed()


def test_scoretools_Container_remove_02():
    r'''Containers remove nested containers correctly.
    Container detaches from parentage.
    Container withdraws from crossing spanners.
    Container carries covered spanners forward.
    Container returns after removal.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    sequential = staff[0]
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:])

    assert testtools.compare(
        staff,
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

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                e'8 [
                f'8 ]
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()

    assert testtools.compare(
        sequential,
        r'''
        {
            c'8
            d'8
        }
        '''
        )

    assert inspect(sequential).is_well_formed()


def test_scoretools_Container_remove_03():
    r'''Container remove works on identity and not equality.
    '''

    note = Note("c'4")
    container = Container([Note("c'4")])

    assert py.test.raises(Exception, 'container.remove(note)')
