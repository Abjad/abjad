# -*- encoding: utf-8 -*-
import pytest
from abjad import *


@pytest.skip()
def test_scoretools_Measure___add___01():
    r'''Add outside-of-score measures.
    '''

    measure_1 = Measure((1, 8), "c'16 d'16")
    beam = Beam()
    attach(beam, measure_1[:])
    measure_2 = Measure((2, 16), "c'16 d'16")
    slur = Slur()
    attach(slur, measure_2[:])
    new = measure_1 + measure_2

    assert systemtools.TestManager.compare(
        new,
        r'''
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
        '''
        )

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0
    assert inspect(new).is_well_formed()


def test_scoretools_Measure___add___02():
    r'''Add measures in score.
    '''

    measure_1 = Measure((1, 8), "c'16 d'16")
    beam = Beam()
    attach(beam, measure_1[:])
    measure_2 = Measure((2, 16), "c'16 d'16")
    slur = Slur()
    attach(slur, measure_2[:])
    staff = Staff([measure_1, measure_2])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                c'16 [
                d'16 ]
            }
            {
                \time 2/16
                c'16 (
                d'16 )
            }
        }
        '''
        )

    new = measure_1 + measure_2

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [
                d'16 ]
                c'16 (
                d'16 )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
