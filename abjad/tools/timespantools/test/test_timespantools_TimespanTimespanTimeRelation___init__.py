# -*- encoding: utf-8 -*-
from abjad import *


def test_timespantools_TimespanTimespanTimeRelation___init___01():
    r'''Initializes timespan / timespan time-relation from empty input.
    '''

    time_relation = timespantools.TimespanTimespanTimeRelation()

    assert systemtools.TestManager.compare(
        format(time_relation, 'storage'),
        r'''
        timespantools.TimespanTimespanTimeRelation(
            inequality=timespantools.CompoundInequality(
                [
                    timespantools.SimpleInequality('timespan_1.start_offset < timespan_2.start_offset'),
                    ],
                logical_operator='and',
                ),
            )
        '''
        )
