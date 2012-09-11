from abjad.tools import sequencetools


def apply_request_transforms(request, resolved_value):
    r'''.. versionadded:: 1.0 
    
    Apply nonnone ``request.index`` to `resolved_value`.

    Apply nonnone ``request.count`` to `resolved_value`.

    Apply nonnone ``request.reverse`` to `resolved_value`.

    Return `resolved_value`.
    '''

    if request.index is not None or request.count is not None:
        original_resolved_value_type = type(resolved_value)
        index = request.index or 0
        if index < 0:
            index = len(resolved_value) - -index
        if request.count is None:
            count = len(resolved_value) - index    
        else:
            count = request.count
        resolved_value = sequencetools.CyclicTuple(resolved_value)
        resolved_value = resolved_value[index:index+count]
        resolved_value = original_resolved_value_type(resolved_value)

    if getattr(request, 'reverse', False):
        original_resolved_value_type = type(resolved_value)
        resolved_value = list(reversed(resolved_value))
        resolved_value = original_resolved_value_type(resolved_value)

    return resolved_value 
