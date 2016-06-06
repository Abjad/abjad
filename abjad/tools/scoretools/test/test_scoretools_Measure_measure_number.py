# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_measure_number_01():
    r'''Measures in staff number correctly starting from 1.
    '''

    time_signature_pairs = [(3, 16), (5, 16), (5, 16)]
    measures = scoretools.make_spacer_skip_measures(time_signature_pairs)
    staff = Staff(measures)

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3


def test_scoretools_Measure_measure_number_02():
    r'''Orphan measures number correctly starting from 1.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    assert measure.measure_number == 1


def test_scoretools_Measure_measure_number_03():
    r'''Measure numbering works correctly after contents rotation.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3

    staff[:] = [staff[1], staff[2], staff[0]]

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                c'8
                d'8
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
