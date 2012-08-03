def selector_to_segment_identifier(selector):
    r'''.. versionadded:: 1.0

    Recurse `selector` and find segment identifier.

    Raise exception when no segment identifier is found.

    .. note:: deprecate. Use ``Selector.segmetn_identifier`` instead.
    '''
    from experimental import selectortools
    
#    if isinstance(selector, selectortools.RatioSelector):
#        segment_identifier = selector.reference.timespan.selector.inequality.timespan.selector.identifier
#    elif isinstance(selector, selectortools.SingleContextTimespanSelector):
#        if isinstance(
#            selector.timespan.selector, selectortools.SegmentItemSelector):
#            segment_identifier = selector.timespan.selector.identifier
#        elif isinstance(
#            selector.timespan.selector, selectortools.BackgroundMeasureSliceSelector):
#            if isinstance(
#                selector.timespan.selector.inequality.timespan.selector,
#                selectortools.SegmentItemSelector):
#                segment_identifier = selector.timespan.selector.inequality.timespan.selector.identifier
#            else:
#                raise NotImplementedError(selector.timespan.selector.inequality.timespan.selector)
#        elif isinstance(
#            selector.timespan.selector, selectortools.DurationRatioItemSelector):
#            if isinstance(
#                selector.timespan.selector.reference.selector,
#                selectortools.SegmentItemSelector):
#                segment_identifier = selector.timespan.selector.reference.selector.identifier
#            else:
#                raise NotImplementedError(selector.timespan.selector.reference.selector)
#        else:
#            raise NotImplementedError(selector.timespan.selector)
#    else:
#        raise NotImplementedError('implement for {!r}.'.format(selector))
#
#    return segment_identifier
