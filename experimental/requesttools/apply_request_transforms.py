from abjad.tools import sequencetools


def apply_request_transforms(request, payload):
    r'''.. versionadded:: 1.0 
    
    In this order:

    Apply nonnone ``request.index`` to `payload`.

    Then apply nonnone ``request.count`` to `payload`.

    Then apply nonnone ``request.reverse`` to `payload`.

    Then apply nonnone ``request.rotation`` to `payload`.

    Return `payload`.
    '''

    if request.index is not None or request.count is not None:
        original_payload_type = type(payload)
        index = request.index or 0
        if index < 0:
            index = len(payload) - -index
        if request.count is None:
            count = len(payload) - index    
        else:
            count = request.count
        payload = sequencetools.CyclicTuple(payload)
        payload = payload[index:index+count]
        payload = original_payload_type(payload)

    if getattr(request, 'reverse', False):
        original_payload_type = type(payload)
        payload = list(reversed(payload))
        payload = original_payload_type(payload)

    if getattr(request, 'rotation', None):
        assert isinstance(request.rotation, int)
        original_payload_type = type(payload)
        payload = sequencetools.rotate_sequence(payload, request.rotation)
        payload = original_payload_type(payload)

    return payload 
