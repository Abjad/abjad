def selector_to_segment_index(selector):
    r'''.. versionadded:: 1.0

    Recurse `selector` and find segment index.

    Raise exception when no segment index is found.
    '''
    from experimental import selectortools
    
    rsc_setting = selector
    if isinstance(rsc_setting.target, selectortools.RatioSelector):
        rsc_setting = rsc_setting
        segment_index = rsc_setting.target.reference.timespan.selector.inequality.timespan.selector.index
    elif isinstance(rsc_setting.target, selectortools.SingleContextTimespanSelector):
        if isinstance(
            rsc_setting.target.timespan.selector, selectortools.SegmentSelector):
            segment_index = rsc_setting.target.timespan.selector.index
        elif isinstance(
            rsc_setting.target.timespan.selector, selectortools.BackgroundMeasureSliceSelector):
            if isinstance(
                rsc_setting.target.timespan.selector.inequality.timespan.selector,
                selectortools.SegmentSelector):
                segment_index = rsc_setting.target.timespan.selector.inequality.timespan.selector.index
            else:
                raise NotImplementedError(rsc_setting.target.timespan.selector.inequality.timespan.selector)
        elif isinstance(
            rsc_setting.target.timespan.selector, selectortools.DurationRatioItemSelector):
            if isinstance(
                rsc_setting.target.timespan.selector.reference.selector,
                selectortools.SegmentSelector):
                segment_index = rsc_setting.target.timespan.selector.reference.selector.index
            else:
                raise NotImplementedError(rsc_setting.target.timespan.selector.reference.selector)
        else:
            raise NotImplementedError(rsc_setting.target.timespan.selector)
    else:
        raise NotImplementedError('implement for {!r}.'.format(rsc_setting.target))

    return segment_index
