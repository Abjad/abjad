def segments_to_timespan(start_segment, stop_segment=None):
    r'''.. versionadded:: 1.0

    Change `start_segment` name to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.segments_to_timespan('red')
        Timespan(CounttimeComponentSelector(segment='red'))

    Change `start_segment` index to timespan::

        >>> specificationtools.segments_to_timespan(0)
        Timespan(CounttimeComponentSelector(segment=0))

    Change segments from `start_segment` name to `stop_segment` name to timespan::

        >>> specificationtools.segments_to_timespan('red', stop_segment='blue')
        Timespan(start=Timepoint(anchor=CounttimeComponentSelector(segment='red'), edge=Left), stop=Timepoint(anchor=CounttimeComponentSelector(segment='blue'), edge=Right))

    Change segments from `start_segment` index to `stop_segment` index to timespan::

        >>> specificationtools.segments_to_timespan(0, stop_segment=3)
        Timespan(start=Timepoint(anchor=CounttimeComponentSelector(segment=0), edge=Left), stop=Timepoint(anchor=CounttimeComponentSelector(segment=3), edge=Right))

    Return timespan.

    .. note:: it is not currently possible to select from segment ``'red'`` forward by
        a count of ``3`` segments total.
    '''
    from experimental import selectortools
    from experimental import specificationtools
    from experimental import timespantools

    if isinstance(start_segment, int):
        pass
    else:
        start_segment = specificationtools.expr_to_segment_name(start_segment)

    start_anchor = selectortools.CounttimeComponentSelector(segment=start_segment)
    start_timepoint = timespantools.Timepoint(anchor=start_anchor, edge=Left)

    if stop_segment is None:
        stop_timepoint = timespantools.Timepoint(anchor=start_anchor, edge=Right)
    else:
        if isinstance(stop_segment, int):
            pass
        else:
            stop_segment = specificationtools.expr_to_segment_name(stop_segment)
        stop_anchor = selectortools.CounttimeComponentSelector(segment=stop_segment)
        stop_timepoint = timespantools.Timepoint(anchor=stop_anchor, edge=Right)

    return timespantools.Timespan(start=start_timepoint, stop=stop_timepoint)
