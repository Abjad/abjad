def request_divisions(start_segment, voice, segment_count=1):
    r'''.. versionadded:: 1.0

    Return division retrieval request.
    '''
    from experimental import selectortools
    from experimental import specificationtools
    
    # process input
    start_segment = selectortools.expr_to_segment_name(start_segment)
    voice = selectortools.expr_to_component_name(voice)

    # populate request
    request = specificationtools.DivisionOldSelector(start_segment, voice, segment_count=segment_count)

    # return request
    return request
