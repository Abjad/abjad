from abjad.tools import contexttools
from experimental.exceptions import *
from experimental.selectortools.TimespanSelector import TimespanSelector
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


class MultipleContextTimespanSelector(TimespanSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select the timespan of segment ``'red'``. Do this for both ``'Voice 1'`` and ``'Voice 3'``.
        
        >>> segment_selector = selectortools.SegmentSelector(index='red')

    ::

        >>> context_names = ['Voice 1', 'Voice 3']
        >>> selector = selectortools.MultipleContextTimespanSelector(context_names, segment_selector.timespan)

    ::

        >>> z(selector)
        selectortools.MultipleContextTimespanSelector(
            context_names=['Voice 1', 'Voice 3'],
            timespan=timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            )

    All mutliple-context timespan selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, context_names=None, timespan=None):
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        # TODO: can we allow both single- and multiple-source timespans?
        assert isinstance(timespan, (SingleSourceTimespan, type(None))), repr(timespan)
        TimespanSelector.__init__(self, timespan=timespan)
        self._context_names = context_names or []

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.context_names == expr.context_names:
                if self.timespan == expr.timespan:
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
