from abjad.tools import contexttools
from experimental.selectortools.MulticontextSelection.MulticontextSelection import MulticontextSelection


class ContextSelection(MulticontextSelection):
    r'''.. versionadded:: 1.0

    Select exactly one context over arbitrary timespan.

    Select ``'Voice 1'`` over segment ``'red'``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> segment_selector = selectortools.SegmentSelector(index='red')

    ::

        >>> context_selection = selectortools.ContextSelection(
        ... 'Voice 1', timespan=segment_selector.timespan)

    ::

        >>> z(context_selection)
        selectortools.ContextSelection(
            'Voice 1',
            timespan=timespantools.Timespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            )

    All context selection properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, context, timespan=None):
        assert isinstance(context, (str, contexttools.Context)), repr(context)
        MulticontextSelection.__init__(self, [context], timespan=timespan)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context(self):
        '''Name of context selection context specified by user::

            >>> context_selection.context
            'Voice 1'

        Return string.
        '''
        return self.contexts[0]
