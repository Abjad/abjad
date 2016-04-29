# -*- coding: utf-8 -*0
from abjad import *


def test_timespantools_OffsetTimespanTimeRelation___init___01():
    r'''Initializes offset / timespan time relation from empty input.
    '''

    time_relation = timespantools.OffsetTimespanTimeRelation()

    assert format(time_relation, 'storage') == stringtools.normalize(
        r'''
        timespantools.OffsetTimespanTimeRelation(
            inequality=timespantools.CompoundInequality(
                [
                    timespantools.Inequality('timespan_1.start_offset < timespan_2.start_offset'),
                    ],
                logical_operator='and',
                ),
            )
        '''
        )
