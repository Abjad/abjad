from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class SegmentSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import selectortools

    ::

        >>> selectortools.SegmentSelector(index=3)
        SegmentSelector(index=3)

    Select segment ``'red'``::

        >>> selectortools.SegmentSelector(index='red')
        SegmentSelector(index='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, index=0):
        from experimental import specificationtools
        BackgroundElementSelector.__init__(self, 
            klass=specificationtools.Segment, inequality=inequality, index=index)
