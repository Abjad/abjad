def segments_to_timespan(start_segment, stop_segment=None):
    r'''.. versionadded:: 1.0

    Change `start_segment` name to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.segments_to_timespan('red')
        Timespan(ScoreObjectSelector(segment='red'))

    Change `start_segment` index to timespan::

        >>> specificationtools.segments_to_timespan(0)
        Timespan(ScoreObjectSelector(segment=0))

    Change segments from `start_segment` name to `stop_segment` name to timespan::

        >>> specificationtools.segments_to_timespan('red', stop_segment='blue')
        Timespan(start=Timepoint(anchor=ScoreObjectSelector(segment='red'), edge=Left), stop=Timepoint(anchor=ScoreObjectSelector(segment='blue'), edge=Right))

    Change segments from `start_segment` index to `stop_segment` index to timespan::

        >>> specificationtools.segments_to_timespan(0, stop_segment=3)
        Timespan(start=Timepoint(anchor=ScoreObjectSelector(segment=0), edge=Left), stop=Timepoint(anchor=ScoreObjectSelector(segment=3), edge=Right))

    Return timespan.

    .. note:: it is not currently possible to select from segment ``'red'`` forward by
        a count of ``3`` segments total.
    '''
    from experimental import specificationtools

    if isinstance(start_segment, int):
        pass
    else:
        start_segment = specificationtools.expr_to_segment_name(start_segment)

    start_anchor = specificationtools.ScoreObjectSelector(segment=start_segment)
    start_timepoint = specificationtools.Timepoint(anchor=start_anchor, edge=Left)

    if stop_segment is None:
        stop_timepoint = specificationtools.Timepoint(anchor=start_anchor, edge=Right)
    else:
        if isinstance(stop_segment, int):
            pass
        else:
            stop_segment = specificationtools.expr_to_segment_name(stop_segment)
        stop_anchor = specificationtools.ScoreObjectSelector(segment=stop_segment)
        stop_timepoint = specificationtools.Timepoint(anchor=stop_anchor, edge=Right)

    return specificationtools.Timespan(start=start_timepoint, stop=stop_timepoint)
