def select_divisions(voice, start_segment, segment_count=1):
    r'''.. versionadded:: 1.0

    Return single-context division slice selector.
    '''
    from experimental import helpertools
    from experimental import selectortools
    from experimental import timespantools
    
    # process input
    start_segment_name = helpertools.expr_to_segment_name(start_segment)
    voice_name = helpertools.expr_to_component_name(voice)

    # make selector
    expression = '{!r} + {}'.format(start_segment_name, segment_count)
    held_expression = helpertools.SegmentIndexExpression(expression)
    start, stop = start_segment_name, held_expression
    selector = selectortools.SegmentSliceSelector(start=start, stop=stop)
    inequality = timespantools.expr_starts_during_timespan(selector.timespan)
    selector = selectortools.SingleContextDivisionSliceSelector(voice_name, inequality=inequality)

    # return selector
    return selector
