def selector_to_segment_identifier(selector):
    r'''.. versionadded:: 1.0

    Recurse `selector` and find segment identifier.

    Raise exception when no segment identifier is found.
    '''
    from experimental import selectortools
    
    # TODO: Change explicit checks to recursive search for SegmentItemSelector.
    if isinstance(selector, selectortools.RatioSelector):
        segment_identifier = selector.reference.timespan.selector.inequality.timespan.selector.index
    elif isinstance(selector, selectortools.SingleContextTimespanSelector):
        if isinstance(
            selector.timespan.selector, selectortools.SegmentItemSelector):
            segment_identifier = selector.timespan.selector.index
        elif isinstance(
            selector.timespan.selector, selectortools.BackgroundMeasureSliceSelector):
            if isinstance(
                selector.timespan.selector.inequality.timespan.selector,
                selectortools.SegmentItemSelector):
                segment_identifier = selector.timespan.selector.inequality.timespan.selector.index
            else:
                raise NotImplementedError(selector.timespan.selector.inequality.timespan.selector)
        elif isinstance(
            selector.timespan.selector, selectortools.DurationRatioItemSelector):
            if isinstance(
                selector.timespan.selector.reference.selector,
                selectortools.SegmentItemSelector):
                segment_identifier = selector.timespan.selector.reference.selector.index
            else:
                raise NotImplementedError(selector.timespan.selector.reference.selector)
        else:
            raise NotImplementedError(selector.timespan.selector)
    else:
        raise NotImplementedError('implement for {!r}.'.format(selector))

    return segment_identifier
