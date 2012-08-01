from experimental.selectortools.BackgroundElementItemSelector import BackgroundElementItemSelector


class SegmentItemSelector(BackgroundElementItemSelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import *

    ::

        >>> selectortools.SegmentItemSelector(index=3)
        SegmentItemSelector(index=3)

    Select segment ``'red'``::

        >>> selectortools.SegmentItemSelector(index='red')
        SegmentItemSelector(index='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, index=0):
        from experimental import specificationtools
        BackgroundElementItemSelector.__init__(self, 
            klass=specificationtools.Segment, inequality=inequality, index=index)

    ### READ-ONLY PROPERTIES ###

    @property
    def context_name(self):
        '''Return none.
        '''
        return

    @property
    def context_names(self):
        '''Return empty list.
        '''
        return []
