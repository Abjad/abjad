from experimental import divisiontools
from experimental.exceptions import *
from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class MultipleContextDivisionSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select the first five divisions starting in segment ``'red'``.
    Do this in both ``'Voice 1'`` and ``'Voice 3'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(segment_selector.timespan)
        >>> division_selector = selectortools.MultipleContextDivisionSliceSelector(
        ... context_names=['Voice 1', 'Voice 3'], inequality=inequality, stop=5)

    ::

        >>> z(division_selector)
        selectortools.MultipleContextDivisionSliceSelector(
            context_names=['Voice 1', 'Voice 3'],
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

    def __init__(self, context_names=None, inequality=None, start=None, stop=None):
        from experimental import interpretertools
        BackgroundElementSliceSelector.__init__(self, divisiontools.Division,
            inequality=inequality, start=start, stop=stop)
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        context_names = self._process_contexts(context_names)
        self._context_names = context_names

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.context_names == expr.context_names:
                if self.inequality == expr.inequality:
                    if self.start == expr.start:
                        if self.stop == expr.stop:
                            return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Raise exception.
        '''
        raise MultipleContextSelectorError

    @property
    def context_names(self):
        '''Return list of context names.
        '''
        return self._context_names
