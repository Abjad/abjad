from experimental import divisiontools
from experimental import helpertools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class SingleContextDivisionSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all ``'Voice 1'`` divisions in score::

        >>> selectortools.SingleContextDivisionSliceSelector('Voice 1')
        SingleContextDivisionSliceSelector('Voice 1')

    Select all ``'Voice 1'`` divisions starting during segment ``'red'``::

        >>> segment = selectortools.SegmentItemSelector(identifier='red')
        >>> timespan = segment.timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> divisions = selectortools.SingleContextDivisionSliceSelector('Voice 1', inequality=inequality)

    ::

        >>> z(divisions)
        selectortools.SingleContextDivisionSliceSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two ``'Voice 1'`` divisions starting during segment ``'red'``::

        >>> divisions = selectortools.SingleContextDivisionSliceSelector('Voice 1', inequality=inequality, start_identifier=-2)

    ::

        >>> z(divisions)
        selectortools.SingleContextDivisionSliceSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, voice, inequality=None, start_identifier=None, stop_identifier=None):
        from experimental import selectortools
        from experimental import interpretertools
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        voice = helpertools.expr_to_component_name(voice)     
        self._voice = voice

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Return string.
        '''
        return self._voice

    @property
    def context_names(self):
        '''Return length-``1`` list.
        '''
        return [self.context_name]

    @property
    def voice(self):
        '''Name of division slice selector voice initialized by user.

        Return string.
        '''
        return self._voice
