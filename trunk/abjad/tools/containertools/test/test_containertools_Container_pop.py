# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_Container_pop_01():
    r'''Containers pop leaves correctly.
    Popped leaves detach from parent.
    Popped leaves withdraw from crossing spanners.
    Popped leaves carry covered spanners forward.
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

    result = voice.pop(1)

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

    assert inspect(voice).is_well_formed()

    "Result is now d'8 [ ]"

    assert inspect(result).is_well_formed()
    assert result.lilypond_format == "d'8 [ ]"


def test_containertools_Container_pop_02():
    r'''Containers pop nested containers correctly.
    Popped containers detach from both parent and spanners.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
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

    sequential = staff.pop()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8 ]
            }
        }
        '''
        )
    assert inspect(staff).is_well_formed()

    assert testtools.compare(
        sequential,
        r'''
        {
            e'8
            f'8
        }
        '''
        )

    assert inspect(sequential).is_well_formed()
