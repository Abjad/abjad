from abjad.tools import durationtools
from abjad.tools import measuretools
from experimental.symbolictimetools.TimeRelationSymbolicTimespan import TimeRelationSymbolicTimespan


class BackgroundMeasureSymbolicTimespan(TimeRelationSymbolicTimespan):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import *

    ::

        >>> symbolictimetools.BackgroundMeasureSymbolicTimespan()
        BackgroundMeasureSymbolicTimespan()

    Select measures from ``3`` forward::

        >>> symbolictimetools.BackgroundMeasureSymbolicTimespan(start_identifier=3)
        BackgroundMeasureSymbolicTimespan(start_identifier=3)

    Select measures up to but not including ``6``::

        >>> symbolictimetools.BackgroundMeasureSymbolicTimespan(stop_identifier=6)
        BackgroundMeasureSymbolicTimespan(stop_identifier=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> symbolictimetools.BackgroundMeasureSymbolicTimespan(start_identifier=3, stop_identifier=6)
        BackgroundMeasureSymbolicTimespan(start_identifier=3, stop_identifier=6)

    Select all measures starting during segment ``'red'``::

        >>> timespan = symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> selector = symbolictimetools.BackgroundMeasureSymbolicTimespan(time_relation=time_relation)

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSymbolicTimespan(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = symbolictimetools.BackgroundMeasureSymbolicTimespan(time_relation=time_relation, start_identifier=-2)

    ::
    
        >>> z(selector)
        symbolictimetools.BackgroundMeasureSymbolicTimespan(
            start_identifier=-2,
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = helpertools.SegmentIdentifierExpression("'red' + 3")
        >>> selector = symbolictimetools.SegmentSymbolicTimespan(start_identifier='red', stop_identifier=expr)
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=selector)

    ::
    
        >>> selector = symbolictimetools.BackgroundMeasureSymbolicTimespan(time_relation=time_relation)

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSymbolicTimespan(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SegmentSymbolicTimespan(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = symbolictimetools.BackgroundMeasureSymbolicTimespan(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSymbolicTimespan(
            start_identifier=-2,
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SegmentSymbolicTimespan(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                )
            )

    Background measure symbolic timespans are immutable.
    '''

    ### INITIALIZER ###

    # TODO: eventually make anchor positional to enforce pervasion ... then make keyword again for data display
    def __init__(self, anchor=None, start_identifier=None, stop_identifier=None, time_relation=None):
        TimeRelationSymbolicTimespan.__init__(self, 
            start_identifier=start_identifier, stop_identifier=stop_identifier, time_relation=time_relation)
        self._anchor = anchor
        self._klass = measuretools.Measure

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: eventually move up to TimeRelationSymbolicTimespan
    @property
    def anchor(self):
        return self._anchor
    
    # TODO: eventually remove in favor of TimeRelationSymbolicTimespan.start_segment_identifier
    @property
    def start_segment_identifier(self):
        return self.anchor

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Evaluate start and stop offsets when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return pair.
        '''
        if start_segment_name is None:
            segment_specification = score_specification.get_start_segment_specification(self)
        else:
            segment_specification = score_specification.get_start_segment_specification(start_segment_name)
        segment_name = segment_specification.segment_name
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        durations = [durationtools.Duration(x) for x in segment_specification.time_signatures]     
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        durations_up_through = durations[:stop]
        duration_up_through = sum(durations_up_through)
        stop_offset = durationtools.Offset(duration_up_through)
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return start_offset, stop_offset

    def get_selected_objects(self, score_specification, context_name):
        '''Get background measures selected when selector is applied
        to `score_specification`.
    
        Ignore `context_name`.

        Return list.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.time_relation.set_segment_identifier()``.
        '''
        assert isinstance(segment_identifier, str)
        if getattr(self.time_relation, 'timespan_1', None) is None:
            self._anchor = segment_identifier
        # TODO: remove this branch after anchor integration
        else:
            self.time_relation.set_segment_identifier(segment_identifier)
