from experimental import divisiontools
from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class MultipleContextDivisionSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import timespantools

    Select the first five divisions starting in segment ``'red'``.
    Do this in both ``'Voice 1'`` and ``'Voice 3'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(segment_selector.timespan)
        >>> division_selector = selectortools.MultipleContextDivisionSliceSelector(
        ... contexts=['Voice 1', 'Voice 3'], inequality=inequality, stop=5)

    ::

        >>> z(division_selector)
        selectortools.MultipleContextDivisionSliceSelector(
            contexts=['Voice 1', 'Voice 3'],
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            stop=5
            )

    ``MultipleContextDivisionSliceSelector`` properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, contexts=None, inequality=None, start=None, stop=None):
        from experimental import interpretertools
        BackgroundElementSliceSelector.__init__(self, divisiontools.Division,
            inequality=inequality, start=start, stop=stop)
        assert isinstance(contexts, (list, type(None))), repr(contexts)
        contexts = self._process_contexts(contexts)
        self._contexts = contexts

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.contexts == expr.contexts:
                if self.inequality == expr.inequality:
                    if self.start == expr.start:
                        if self.stop == expr.stop:
                            return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        return self._contexts
