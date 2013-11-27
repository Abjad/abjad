# -*- encoding: utf-8 -*0
from abjad import *


def test_timerelationtools_OffsetTimespanTimeRelation___init___01():
    r'''Initializes offset / timespan time relation from empty input.
    '''

    time_relation = timerelationtools.OffsetTimespanTimeRelation()

    assert systemtools.TestManager.compare(
        format(time_relation, 'storage'),
        r'''
        timerelationtools.OffsetTimespanTimeRelation(
            inequality=timerelationtools.CompoundInequality(
                [
                    timerelationtools.SimpleInequality('timespan_1.start_offset < timespan_2.start_offset'),
                    ],
                logical_operator='and',
                ),
            )
        '''
        )
