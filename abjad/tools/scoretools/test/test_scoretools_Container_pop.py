# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Container_pop_01():
    r'''Containers pop leaves correctly.
    Popped leaves detach from parent.
    Popped leaves withdraw from crossing spanners.
    Popped leaves carry covered spanners forward.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, voice[:])
    beam = Beam()
    attach(beam, voice[1])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 (
            e'8
            f'8 )
        }
        '''
        )

    assert inspect_(voice).is_well_formed()

    "Result is now d'8 [ ]"

    assert inspect_(result).is_well_formed()
    assert format(result) == "d'8 [ ]"


def test_scoretools_Container_pop_02():
    r'''Containers pop nested containers correctly.
    Popped containers detach from both parent and spanners.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff[:])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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
    assert inspect_(staff).is_well_formed()

    assert systemtools.TestManager.compare(
        sequential,
        r'''
        {
            e'8
            f'8
        }
        '''
        )

    assert inspect_(sequential).is_well_formed()