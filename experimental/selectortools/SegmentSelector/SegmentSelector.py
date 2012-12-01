from experimental import helpertools
from experimental import segmenttools
from experimental.selectortools.TimeRelationSelector import TimeRelationSelector
from experimental.selectortools.SliceSelector import SliceSelector


class SegmentSelector(SliceSelector, TimeRelationSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> selectortools.SegmentSelector()
        SegmentSelector()

    Select segments from ``3`` forward::

        >>> selectortools.SegmentSelector(start_identifier=3)
        SegmentSelector(start_identifier=3)

    Select segments up to but not including ``6``::

        >>> selectortools.SegmentSelector(stop_identifier=6)
        SegmentSelector(stop_identifier=6)

    Select segments up to and including ``6``::

        >>> selectortools.SegmentSelector(stop_identifier=6+1)
        SegmentSelector(stop_identifier=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> selectortools.SegmentSelector(start_identifier=3, stop_identifier=6)
        SegmentSelector(start_identifier=3, stop_identifier=6)

    Select segments from ``3`` up to and including ``6``::

        >>> selectortools.SegmentSelector(start_identifier=3, stop_identifier=6+1)
        SegmentSelector(start_identifier=3, stop_identifier=7)

    Select segments from ``'red'`` forward::

        >>> selectortools.SegmentSelector(start_identifier='red')
        SegmentSelector(start_identifier='red')

    Select segments up to but not including ``'blue'``::

        >>> selectortools.SegmentSelector(stop_identifier='blue')
        SegmentSelector(stop_identifier='blue')

    Select segments up to and including ``'blue'``::

        >>> selectortools.SegmentSelector(stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier='blue')
        SegmentSelector(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> selectortools.SegmentSelector(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3"))
        SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    Select all segments starting during the first third of the score:

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> selector = selectortools.SegmentSelector(time_relation=time_relation)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    multiplier=durationtools.Multiplier(1, 3)
                    )
                )
            )

    Select the last two segments starting during the first third of the score::

        >>> selector = selectortools.SegmentSelector(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.SegmentSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    multiplier=durationtools.Multiplier(1, 3)
                    )
                ),
            start_identifier=-2
            )

    All segment selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, start_identifier=None, stop_identifier=None, voice_name=None):
        SliceSelector.__init__(
            self, start_identifier=start_identifier, stop_identifier=stop_identifier, voice_name=voice_name)
        TimeRelationSelector.__init__(self, time_relation=time_relation)
        self._klass = segmenttools.Segment

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier

    ### PUBLIC PROPERTIES ###

    def get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.

        Ignore `context_name`.

        Return offset.
        '''
        return score_specification.segment_identifier_expression_to_offsets(self.start_segment_identifier)

    def get_selected_objects(self, score_specification, context_name):
        '''Get segments selected when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return list of segments.
        '''
        raise NotImplementedError
