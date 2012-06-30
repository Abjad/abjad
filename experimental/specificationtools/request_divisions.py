def request_divisions(start_segment, voice, segment_count=1):
    r'''.. versionadded:: 1.0

    Return division retrieval request.
    '''
    from experimental import specificationtools
    
    # process input
    start_segment = specificationtools.expr_to_segment_name(start_segment)
    voice = specificationtools.expr_to_component_name(voice)

    # populate request
    request = specificationtools.DivisionSelector(start_segment, voice, segment_count=segment_count)

    # return request
    return request
