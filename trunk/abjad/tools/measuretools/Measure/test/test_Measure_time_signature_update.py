# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_time_signature_update_01():
    r'''Measures allow time signature update.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

    measure.pop()
    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((3, 8))(measure)

    assert testtools.compare(
        measure,
        r'''
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        '''
        )

    assert select(measure).is_well_formed()
