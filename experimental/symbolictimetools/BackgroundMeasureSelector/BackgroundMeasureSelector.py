from abjad.tools import durationtools
from abjad.tools import measuretools
from experimental.symbolictimetools.Selector import Selector


class BackgroundMeasureSelector(Selector):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import *

    ::

        >>> symbolictimetools.BackgroundMeasureSelector()
        BackgroundMeasureSelector()

    Select measures from ``3`` forward::

        >>> symbolictimetools.BackgroundMeasureSelector(start_identifier=3)
        BackgroundMeasureSelector(start_identifier=3)

    Select measures up to but not including ``6``::

        >>> symbolictimetools.BackgroundMeasureSelector(stop_identifier=6)
        BackgroundMeasureSelector(stop_identifier=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> symbolictimetools.BackgroundMeasureSelector(start_identifier=3, stop_identifier=6)
        BackgroundMeasureSelector(start_identifier=3, stop_identifier=6)

    Select all measures starting during segment ``'red'``::

        >>> selector = symbolictimetools.BackgroundMeasureSelector(anchor='red')

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSelector(
            anchor='red'
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = symbolictimetools.BackgroundMeasureSelector(anchor='red', start_identifier=-2)

    ::
    
        >>> z(selector)
        symbolictimetools.BackgroundMeasureSelector(
            anchor='red',
            start_identifier=-2
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = helpertools.SegmentIdentifierExpression("'red' + 3")
        >>> selector = symbolictimetools.SegmentSelector(start_identifier='red', stop_identifier=expr)
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=selector)

    ::
    
        >>> selector = symbolictimetools.BackgroundMeasureSelector(time_relation=time_relation)

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SegmentSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = symbolictimetools.BackgroundMeasureSelector(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(selector)
        symbolictimetools.BackgroundMeasureSelector(
            start_identifier=-2,
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SegmentSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                )
            )

    Background measure symbolic timespans are immutable.
    '''

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Evaluate start and stop offsets when selector is applied
        to `score_specification`.

        Ignore `context_name`. 

        Maybe eventually ignore start_segment_name and use anchor instead.

        Return pair.
        '''
        #self._debug(self.offset_modifications, 'offset modifications')
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        segment_name = segment_specification.segment_name
        #self._debug(self.identifiers, 'identifiers')
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
        #self._debug((start_offset, stop_offset), 'offsets')
        return start_offset, stop_offset

    def get_selected_objects(self, score_specification, context_name):
        '''Get background measures selected when selector is applied
        to `score_specification`.
    
        Ignore `context_name`.

        Return list of nonreduced fractions.
        '''
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        segment_name = segment_specification.segment_name
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        time_signatures = segment_specification.time_signatures
        time_signatures = time_signatures[start:stop]
        return time_signatures

    def set_segment_identifier(self, segment_identifier):
        '''Set anchor to `segment_identifier`.
        '''
        assert isinstance(segment_identifier, str)
        assert not hasattr(self.time_relation, 'timespan_1')
        self._anchor = segment_identifier
