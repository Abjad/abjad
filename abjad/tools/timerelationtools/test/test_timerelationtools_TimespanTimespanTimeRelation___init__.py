# -*- encoding: utf-8 -*-
from abjad import *


def test_timerelationtools_TimespanTimespanTimeRelation___init___01():
    r'''Initializes timespan / timespan time-relation from empty input.
    '''

    time_relation = timerelationtools.TimespanTimespanTimeRelation()

    assert systemtools.TestManager.compare(
        format(time_relation, 'storage'),
        r'''
        timerelationtools.TimespanTimespanTimeRelation(
            inequality=timerelationtools.CompoundInequality(
                [
                    timerelationtools.SimpleInequality('timespan_1.start_offset < timespan_2.start_offset'),
                    ],
                logical_operator='and',
                ),
            )
        '''
        )
