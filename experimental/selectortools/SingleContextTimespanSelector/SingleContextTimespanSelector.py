from abjad.tools import contexttools
from experimental.selectortools.TimespanSelector import TimespanSelector


class SingleContextTimespanSelector(TimespanSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    Select the timespan of segment ``'red'`` in ``'Voice 1'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')

    ::

        >>> selector = selectortools.SingleContextTimespanSelector('Voice 1', timespan=segment_selector.timespan)

    ::

        >>> z(selector)
        selectortools.SingleContextTimespanSelector(
            'Voice 1',
            timespan=timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            )

    All single-context timespan selector properties are read-only.
    '''

    ### INITIALIZER ###

    # TODO: make 'timespan' argument mandatory
    def __init__(self, context, timespan=None):
        assert isinstance(context, (str, contexttools.Context)), repr(context)
        TimespanSelector.__init__(self, timespan=timespan)
        self._context = context

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.context == expr.context:
                if self.timespan == expr.timespan:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context(self):
        '''Context name of selector specified by user::

            >>> selector.context
            'Voice 1'

        Return string.
        '''
        return self._context
