from experimental.specificationtools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class SegmentSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    Select all segments::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.SegmentSliceSelector()
        SegmentSliceSelector()

    Select segments from ``3`` forward::

        >>> specificationtools.SegmentSliceSelector(start=3)
        SegmentSliceSelector(start=3)

    Select segments up to but not including ``6``::

        >>> specificationtools.SegmentSliceSelector(stop=6)
        SegmentSliceSelector(stop=6)

    Select segments up to and including ``6``::

        >>> specificationtools.SegmentSliceSelector(stop=6+1)
        SegmentSliceSelector(stop=7)

    Select segments from ``3`` up to but not including ``6``::

        >>> specificationtools.SegmentSliceSelector(start=3, stop=6)
        SegmentSliceSelector(start=3, stop=6)

    Select segments from ``3`` up to and including ``6``::

        >>> specificationtools.SegmentSliceSelector(start=3, stop=6+1)
        SegmentSliceSelector(start=3, stop=7)

    Select segments from ``'red'`` forward::

        >>> specificationtools.SegmentSliceSelector(start='red')
        SegmentSliceSelector(start='red')

    Select segments up to but not including ``'blue'``::

        >>> specificationtools.SegmentSliceSelector(stop='blue')
        SegmentSliceSelector(stop='blue')

    Select segments up to and including ``'blue'``::

        >>> specificationtools.SegmentSliceSelector(stop=specificationtools.Hold("'blue' + 1"))
        SegmentSliceSelector(stop=Hold("'blue' + 1"))

    Select segments from ``'red'`` up to but not including ``'blue'``::

        >>> specificationtools.SegmentSliceSelector(start='red', stop='blue')
        SegmentSliceSelector(start='red', stop='blue')

    Select segments from ``'red'`` up to and including ``'blue'``::

        >>> specificationtools.SegmentSliceSelector(start='red', stop=specificationtools.Hold("'blue' + 1"))
        SegmentSliceSelector(start='red', stop=Hold("'blue' + 1"))

    Select three segments from ``'red'``::

        >>> specificationtools.SegmentSliceSelector(start='red', stop=specificationtools.Hold("'red' + 3"))
        SegmentSliceSelector(start='red', stop=Hold("'red' + 3"))

    Select all segments starting during the first third of the score:

        >>> 

    Segment slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start=None, stop=None):
        from experimental import specificationtools
        BackgroundElementSliceSelector.__init__(self, specificationtools.Segment,
            inequality=inequality, start=start, stop=stop)
