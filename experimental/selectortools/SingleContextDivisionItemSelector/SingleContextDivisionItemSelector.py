from experimental import divisiontools
from experimental import helpertools
from experimental.selectortools.BackgroundElementItemSelector import BackgroundElementItemSelector


class SingleContextDivisionItemSelector(BackgroundElementItemSelector):
    r'''.. versionadded:: 1.0

    Select division ``3`` in ``'Voice 1'``::

        >>> from experimental import *

    ::

        >>> selectortools.SingleContextDivisionItemSelector('Voice 1', identifier=3)
        SingleContextDivisionItemSelector('Voice 1', identifier=3)

    Select the last ``'Voice 1'`` division to start during segment ``'red'``::

        >>> timespan = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.SingleContextDivisionItemSelector('Voice 1', inequality=inequality, identifier=-1)

    ::

        >>> z(selector)
        selectortools.SingleContextDivisionItemSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            identifier=-1
            )

    Select the last ``'Voice 1'`` division to start during the last measure to start during 
    segment ``'red'``::

        >>> timespan = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)
        >>> measure = selectortools.BackgroundMeasureItemSelector(inequality=inequality, identifier=-1)

    ::
        
        >>> timespan = measure
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)
        >>> division = selectortools.SingleContextDivisionItemSelector('Voice 1', inequality=inequality, identifier=-1)

    ::

        >>> z(division)
        selectortools.SingleContextDivisionItemSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.BackgroundMeasureItemSelector(
                        inequality=timespantools.TimespanInequality(
                            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                            timespantools.SingleSourceTimespan(
                                selector=selectortools.SegmentItemSelector(
                                    identifier='red'
                                    )
                                )
                            ),
                        identifier=-1
                        )
                    )
                ),
            identifier=-1
            )

    Division selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, voice, inequality=None, identifier=0):
        from experimental import selectortools
        from experimental import interpretertools
        BackgroundElementItemSelector.__init__(
            self, klass=divisiontools.Division, identifier=identifier, inequality=inequality)
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
        '''Name of division selector voice initialized by user.

        Return string.
        '''
        return self._voice
