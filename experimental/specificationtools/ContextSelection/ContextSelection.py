from abjad.tools import contexttools
from experimental.specificationtools.Selection.Selection import Selection


class ContextSelection(Selection):
    r'''.. versionadded:: 1.0

    Select exactly one context over arbitrary timespan.

    Select ``'Voice 1'`` over segment ``'red'``::

        >>> anchor = selectortools.SegmentSelector(index='red')
        >>> start = timespantools.Timepoint(anchor=anchor)
        >>> stop = timespantools.Timepoint(anchor=anchor, edge=Right)
        >>> timespan = timespantools.Timespan(start=start, stop=stop)

    ::

        >>> context_selection = specificationtools.ContextSelection('Voice 1', timespan=timespan)

    ::

        >>> z(context_selection)
        specificationtools.ContextSelection(
            'Voice 1',
            timespan=timespantools.Timespan(
                start=timespantools.Timepoint(
                    anchor=selectortools.SegmentSelector(
                        index='red'
                        )
                    ),
                stop=timespantools.Timepoint(
                    anchor=selectortools.SegmentSelector(
                        index='red'
                        ),
                    edge=Right
                    )
                )
            )

    Context selections are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, context, timespan=None):
        assert isinstance(context, (str, contexttools.Context)), repr(context)
        Selection.__init__(self, [context], timespan=timespan)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context(self):
        '''Name of context selection context specified by user::

            >>> context_selection.context
            'Voice 1'

        Return string.
        '''
        return self.contexts[0]
