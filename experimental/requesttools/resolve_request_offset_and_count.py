from abjad.tools import sequencetools


def resolve_request_offset_and_count(request, resolved_value):
    r'''..versionadded:: 1.0 
    
    Find `request` offset and count.

    If either is not none, apply to `resolved_value`.

    Return modified (or unmodified) `resolved_value`.
    '''

    if request.offset is not None or request.count is not None:
        original_resolved_value_type = type(resolved_value)
        offset = request.offset or 0
        if offset < 0:
            offset = len(resolved_value) - -offset
        if request.count is None:
            count = len(resolved_value) - offset    
        else:
            count = request.count
        resolved_value = sequencetools.CyclicTuple(resolved_value)
        result = resolved_value[offset:offset+count]
        result = original_resolved_value_type(result)
        return result
    else:
        return resolved_value
