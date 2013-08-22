# -*- encoding: utf-8 -*-
from abjad import *


def test_TrillSpanner_pitch_01():
    r'''Assign Abjad pitch instance to create a pitched trill.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner(staff[:2])
    trill.pitch = pitchtools.NamedPitch(1)

    r'''
    \new Staff {
        \pitchedTrill
        c'8 \startTrillSpan cs'
        d'8 \stopTrillSpan
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \pitchedTrill
            c'8 \startTrillSpan cs'
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )


def test_TrillSpanner_pitch_02():
    r'''Any pitch init value will work.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner(staff[:2])
    trill.pitch = 1

    r'''
    \new Staff {
        \pitchedTrill
        c'8 \startTrillSpan cs'
        d'8 \stopTrillSpan
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \pitchedTrill
            c'8 \startTrillSpan cs'
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )


def test_TrillSpanner_pitch_03():
    r'''Clear with None.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner(staff[:2])
    trill.pitch = pitchtools.NamedPitch(1)
    trill.pitch = None

    r'''
    \new Staff {
        c'8 \startTrillSpan
        d'8 \stopTrillSpan
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \startTrillSpan
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )
