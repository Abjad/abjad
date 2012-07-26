from abjad.tools import sequencetools


def resolve_request_offset_and_count(request, value):
    r'''..versionadded:: 1.0 
    
    Resolve `request` offset and count.

    Return something from `value`.
    '''
    if request.offset is not None or request.count is not None:
        original_value_type = type(value)
        offset = request.offset or 0
        count = request.count or 0
        value = sequencetools.CyclicTuple(value)
        if offset < 0:
            offset = len(value) - -offset
        result = value[offset:offset+count]
        result = original_value_type(result)
        return result
    else:
        return value
