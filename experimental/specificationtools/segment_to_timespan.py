def segment_to_timespan(segment):
    r'''.. versionadded:: 1.0

    Change `segment` to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.segment_to_timespan('red')
        Timespan(ScoreObjectIndicator(segment='red'))

    Return timespan.
    '''
    from experimental import specificationtools

    if isinstance(segment, specificationtools.SegmentSpecification):
        segment = segment.name
    elif not isinstance(segment, str):
        raise Exception('{!r} is neither a segment nor a segment name.'.format(segment))

    anchor = specificationtools.ScoreObjectIndicator(segment=segment)

    start = specificationtools.Timepoint(anchor=anchor)
    stop = specificationtools.Timepoint(anchor=anchor, edge=Right)

    return specificationtools.Timespan(start=start, stop=stop)
