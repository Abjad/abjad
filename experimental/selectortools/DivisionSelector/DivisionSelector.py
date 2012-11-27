from abjad.tools import durationtools
from experimental import divisiontools
from abjad.tools import timerelationtools
from experimental.selectortools.TimeRelationSelector import TimeRelationSelector
from experimental.selectortools.SliceSelector import SliceSelector


class DivisionSelector(SliceSelector, TimeRelationSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all divisions::

        >>> selectortools.DivisionSelector()
        DivisionSelector()

    Select all divisions that start during segment ``'red'``::

        >>> red_segment = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan = red_segment.timespan
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> division_selector = selectortools.DivisionSelector(time_relation=time_relation)

    ::

        >>> z(division_selector)
        selectortools.DivisionSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two divisions that start during segment ``'red'``::

        >>> division_selector = selectortools.DivisionSelector(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(division_selector)
        selectortools.DivisionSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, start_identifier=None, stop_identifier=None, voice_name=None):
        SliceSelector.__init__(
            self, start_identifier=start_identifier, stop_identifier=stop_identifier, voice_name=voice_name)
        TimeRelationSelector.__init__(self, time_relation=time_relation)
        self._klass = divisiontools.Division

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    ### PUBLIC METHODS ###

    # TODO: eventually merge with CounttimeComponentSelector.get_offsets()
    def get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selecto when applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return pair.
        '''
        divisions = self.get_selected_objects(score_specification, voice_name)
        start_offset = divisions[0].start_offset
        stop_offset = divisions[-1].stop_offset
        return start_offset, stop_offset
        
    # TODO: eventually return selection
    def get_selected_objects(self, score_specification, voice_name):
        '''Get divisions selected when selector is applied
        to `voice_name` in `score_specification`.

        .. note:: add example.
        
        Return list of zero or more offset-positioned divisions.
        '''
        voice_division_list = score_specification.contexts[voice_name]['voice_division_list']
        divisions = []
        for division in voice_division_list:
            if self.time_relation is None or self.time_relation(timespan_2=division, 
                score_specification=score_specification, context_name=voice_name):
                divisions.append(division)
        divisions = divisions[self.start_identifier:self.stop_identifier]
        return divisions
    
    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.time_relation.set_segment_identifier()``.
        '''
        self.time_relation.set_segment_identifier(segment_identifier)
