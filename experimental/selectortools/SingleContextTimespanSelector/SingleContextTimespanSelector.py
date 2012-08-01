from abjad.tools import contexttools
from experimental.selectortools.TimespanSelector import TimespanSelector


class SingleContextTimespanSelector(TimespanSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select the timespan of segment ``'red'`` in ``'Voice 1'``::

        >>> segment_selector = selectortools.SegmentItemSelector(index='red')

    ::

        >>> selector = selectortools.SingleContextTimespanSelector('Voice 1', segment_selector.timespan)

    ::

        >>> z(selector)
        selectortools.SingleContextTimespanSelector(
            'Voice 1',
            timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentItemSelector(
                    index='red'
                    )
                )
            )

    All single-context timespan selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, context_name, timespan):
        assert isinstance(context_name, str), repr(context_name)
        TimespanSelector.__init__(self, timespan=timespan)
        self._context_name = context_name

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.context_name == expr.context_name:
                if self.timespan == expr.timespan:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Context name of selector specified by user::

            >>> selector.context_name
            'Voice 1'

        Return string.
        '''
        return self._context_name

    @property
    def context_names(self):
        '''Return length-``1`` list.
        '''
        return [self.context_name]
