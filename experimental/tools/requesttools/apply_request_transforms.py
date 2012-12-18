import copy
from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools


def apply_request_transforms(request, payload):
    r'''.. versionadded:: 1.0 
    
    In this order:

    Apply nonnone ``request.index`` to `payload`.

    Then apply nonnone ``request.count`` to `payload`.

    Then apply nonnone ``request.reverse`` to `payload`.

    Then apply nonnone ``request.rotation`` to `payload`.
    
    Return `payload`.
    '''
    from experimental.tools import interpretertools
    from experimental.tools import requesttools
    from experimental.tools import settingtools

    request_klasses = (
        requesttools.Request, 
        settingtools.Setting, 
        settingtools.Command,
        )

    #print request
    #print payload
    #print ''

    assert isinstance(request, request_klasses), repr(request)
    assert isinstance(payload, (list, tuple, rhythmmakertools.RhythmMaker)), repr(payload)

    #assert hasattr(request, 'modifications')
    if hasattr(request, 'modifications'):
        for modification in request.modifications:
            assert 'target' in modification
            target = copy.deepcopy(payload)
            eval(modification)
            payload = target

    if isinstance(payload, rhythmmakertools.RhythmMaker):
        if request.reverse:
            payload = payload.reverse()
        return payload

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

    if request.reverse:
        original_payload_type = type(payload)
        payload = list(reversed(payload))
        payload = original_payload_type(payload)

    if request.rotation:
        assert isinstance(request.rotation, int)
        original_payload_type = type(payload)
        payload = sequencetools.rotate_sequence(payload, request.rotation)
        payload = original_payload_type(payload)

    return payload 
