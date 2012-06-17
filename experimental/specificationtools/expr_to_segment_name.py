def expr_to_segment_name(segment):
    r'''.. versionadded:: 1.0
    
    Change `segment` to segment name. Return string unchanged.

    Return string.
    '''
    from experimental import specificationtools
    if isinstance(segment, specificationtools.SegmentSpecification):
        return segment.name
    elif isinstance(segment, str):
        return segment
    else:
        raise Exception('{!r} is neither segment nor string.'.format(segment))
