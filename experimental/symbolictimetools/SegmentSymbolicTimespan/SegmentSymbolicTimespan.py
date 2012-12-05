from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.TimeRelationSymbolicTimespan import TimeRelationSymbolicTimespan


class SegmentSymbolicTimespan(TimeRelationSymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all segments in score::

        >>> symbolictimetools.SegmentSymbolicTimespan()
        SegmentSymbolicTimespan()

    Select segments from ``3`` forward::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier=3)
        SegmentSymbolicTimespan(start_identifier=3)

    Select segments up to but not including ``6``::

        >>> symbolictimetools.SegmentSymbolicTimespan(stop_identifier=6)
        SegmentSymbolicTimespan(stop_identifier=6)

    Select segments up to and including ``6``::

        >>> symbolictimetools.SegmentSymbolicTimespan(stop_identifier=6+1)
        SegmentSymbolicTimespan(stop_identifier=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier=3, stop_identifier=6)
        SegmentSymbolicTimespan(start_identifier=3, stop_identifier=6)

    Select segments from ``3`` up to and including ``6``::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier=3, stop_identifier=6+1)
        SegmentSymbolicTimespan(start_identifier=3, stop_identifier=7)

    Select segments from ``'red'`` forward::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier='red')
        SegmentSymbolicTimespan(start_identifier='red')

    Select segments up to but not including ``'blue'``::

        >>> symbolictimetools.SegmentSymbolicTimespan(stop_identifier='blue')
        SegmentSymbolicTimespan(stop_identifier='blue')

    Select segments up to and including ``'blue'``::

        >>> symbolictimetools.SegmentSymbolicTimespan(stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSymbolicTimespan(stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier='red', stop_identifier='blue')
        SegmentSymbolicTimespan(start_identifier='red', stop_identifier='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1"))
        SegmentSymbolicTimespan(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> symbolictimetools.SegmentSymbolicTimespan(start_identifier='red', stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3"))
        SegmentSymbolicTimespan(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

    Select all segments starting during the first third of the score:

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> selector = symbolictimetools.SegmentSymbolicTimespan(time_relation=time_relation)

    ::

        >>> z(selector)
        symbolictimetools.SegmentSymbolicTimespan(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    multiplier=durationtools.Multiplier(1, 3)
                    )
                )
            )

    Select the last two segments starting during the first third of the score::

        >>> selector = symbolictimetools.SegmentSymbolicTimespan(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(selector)
        symbolictimetools.SegmentSymbolicTimespan(
            start_identifier=-2,
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                    multiplier=durationtools.Multiplier(1, 3)
                    )
                )
            )

    All segment selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start_identifier=None, stop_identifier=None, time_relation=None):
        from experimental import specificationtools
        TimeRelationSymbolicTimespan.__init__(self, 
            start_identifier=start_identifier, stop_identifier=stop_identifier, time_relation=time_relation)
        self._klass = specificationtools.SegmentSpecification

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Always anchored to timespan of score.

        Return none.
        ''' 
        return

    @property
    def start_segment_identifier(self):
        '''Temporary hack. Generalize later.
        '''
        return self.start_identifier

    ### PUBLIC PROPERTIES ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
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
