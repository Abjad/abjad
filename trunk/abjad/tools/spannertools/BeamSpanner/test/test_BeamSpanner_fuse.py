# -*- encoding: utf-8 -*-
from abjad import *


def test_BeamSpanner_fuse_01():
    r'''Fuse beams.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    left_beam = spannertools.BeamSpanner(staff[:2])
    right_beam = spannertools.BeamSpanner(staff[2:4])
    left_beam.fuse(right_beam)

    assert testtools.compare(
        staff,
        r'''
            
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
