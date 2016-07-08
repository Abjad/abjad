# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_MeasuredComplexBeam_direction_01():

    staff = Staff("abj: | 2/16 c'16 d'16 || 2/16 e'16 f'16 |"
        "| 2/16 g'16 a'16 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/16
                c'16
                d'16
            }
            {
                e'16
                f'16
            }
            {
                g'16
                a'16
            }
        }
        '''
        )

    leaves = select(staff).by_leaf()
    beam = spannertools.MeasuredComplexBeam(direction=Down)
    attach(beam, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/16
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 _ [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                d'16
            }
            {
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                f'16
            }
            {
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                g'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                a'16 ]
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
