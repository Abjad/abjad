from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class DivisionSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0

    Select division ``3`` in ``'Voice 1'``::

        >>> from experimental import selectortools

    ::

        >>> selectortools.DivisionSelector('Voice 1', index=3)
        DivisionSelector('Voice 1', index=3)

    Select the last ``'Voice 1'`` division to start during segment ``'red'``::

        >>> from experimental import timespantools

    ::

        >>> timespan = selectortools.SegmentSelector(index='red').timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.DivisionSelector('Voice 1', inequality=inequality, index=-1)

    ::

        >>> z(selector)
        selectortools.DivisionSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            index=-1
            )

    Select the last ``'Voice 1'`` division to start during the last measure to start during 
    segment ``'red'``::

        >>> timespan = selectortools.SegmentSelector(index='red').timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)
        >>> measure = selectortools.BackgroundBackgroundMeasureSelector(inequality=inequality, index=-1)

    ::
        
        >>> timespan = measure.timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)
        >>> division = selectortools.DivisionSelector('Voice 1', inequality=inequality, index=-1)

    ::

        >>> z(division)
        selectortools.DivisionSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.BackgroundBackgroundMeasureSelector(
                        inequality=timespantools.TimespanInequality(
                            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                            timespantools.Timespan(
                                selector=selectortools.SegmentSelector(
                                    index='red'
                                    )
                                )
                            ),
                        index=-1
                        )
                    )
                ),
            index=-1
            )

    Division selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, voice, inequality=None, index=0):
        from abjad.tools import voicetools
        from experimental import specificationtools
        BackgroundElementSelector.__init__(
            self, klass=specificationtools.Division, index=index, inequality=inequality)
        voice = specificationtools.expr_to_component_name(voice)
        self._voice = voice

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def voice(self):
        '''Name of division selector voice initialized by user.

        Return string.
        '''
        return self._voice
