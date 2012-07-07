def segments_to_timespan(start_segment, stop_segment=None):
    r'''.. versionadded:: 1.0

    Select the timespan of segment ``'red'``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.segments_to_timespan('red')
        Timespan(selector=SegmentSelector(index='red'))

    Select the timespan of segment ``0``::

        >>> specificationtools.segments_to_timespan(0)
        Timespan(selector=SegmentSelector(index=0))

    Select the timespan of segments ``'red'`` to ``'blue'``::

        >>> specificationtools.segments_to_timespan('red', stop_segment='blue')
        Timespan(selector=SegmentSliceSelector(start='red', stop='blue'))

    Select the timespan of segments ``0`` to ``3``::

        >>> specificationtools.segments_to_timespan(0, stop_segment=3)
        Timespan(selector=SegmentSliceSelector(start=0, stop=3))

    Return timespan.

    .. note:: with this function it is not currently possible to select from 
        segment ``'red'`` forward by a count of ``3`` segments total. 
        It is possible to do this with the ``SegmentSliceSelector`` class.

    .. note:: may be better to deprecate this function in favor of
        the ``SegmentSliceSelector`` class.
    '''
    from experimental import selectortools
    from experimental import specificationtools
    from experimental import timespantools

    if isinstance(start_segment, int):
        start_segment_index = start_segment
    else:
        start_segment_index = specificationtools.expr_to_segment_name(start_segment)

    if stop_segment is None:
        segment_selector = selectortools.SegmentSelector(index=start_segment_index)
        timespan = segment_selector.timespan
    else:
        if isinstance(stop_segment, int):
            stop_segment_index = stop_segment
        else:
            stop_segment_index = specificationtools.expr_to_segment_name(stop_segment)
        segment_slice_selector = selectortools.SegmentSliceSelector(
            start=start_segment_index, stop=stop_segment_index)
        timespan = segment_slice_selector.timespan

    return timespan
