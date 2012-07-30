from abjad.tools import contexttools
from experimental.selectortools.TimespanSelector import TimespanSelector
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


class MultipleContextTimespanSelector(TimespanSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    Select the timespan of segment ``'red'``. Do this for both ``'Voice 1'`` and ``'Voice 3'``.
        
        >>> segment_selector = selectortools.SegmentSelector(index='red')

    ::

        >>> contexts = ['Voice 1', 'Voice 3']
        >>> selector = selectortools.MultipleContextTimespanSelector(contexts, segment_selector.timespan)

    ::

        >>> z(selector)
        selectortools.MultipleContextTimespanSelector(
            contexts=['Voice 1', 'Voice 3'],
            timespan=timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            )

    All mutliple-context timespan selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, contexts=None, timespan=None):
        assert isinstance(contexts, (list, type(None))), repr(contexts)
        # TODO: can we allow both single- and multiple-source timespans?
        assert isinstance(timespan, (SingleSourceTimespan, type(None))), repr(timespan)
        TimespanSelector.__init__(self, timespan=timespan)
        self._contexts = contexts

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.contexts == expr.contexts:
                if self.timespan == expr.timespan:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        '''Contexts specified by user.

        Value of none taken equal to all contexts in score.

        Return list of strings or none.
        '''
        return self._contexts
