# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_TrillSpanner_pitch_01():
    r'''Works with pitch.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner(pitch=NamedPitch(1))
    attach(trill, staff[:2])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_TrillSpanner_pitch_02():
    r'''Works with no pitch.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner()
    attach(trill, staff[:2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 \startTrillSpan
            d'8 \stopTrillSpan
            e'8
            f'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
