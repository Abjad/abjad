import copy
from abjad.tools import rhythmmakertools


def apply_request_transforms(request, payload):
    r'''.. versionadded:: 1.0 
    
    Apply `request` modifications to `payload`.

    Return modified `payload` copy.
    '''
    from experimental.tools import requesttools
    from experimental.tools import symbolictimetools

    request_klasses = (
        requesttools.Request, 
        symbolictimetools.VoiceSelector,
        )

    assert isinstance(request, request_klasses), repr(request)
    assert isinstance(payload, (list, tuple, rhythmmakertools.RhythmMaker)), repr(payload)
    assert hasattr(request, 'modifications')

    for modification in request.modifications:
        assert 'target' in modification
        target = copy.deepcopy(payload)
        exec(modification)
        if result is None:
            payload = target
        else:
            payload = result

    return payload 
