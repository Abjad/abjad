import copy
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools


def apply_modifications(request, payload):
    r'''.. versionadded:: 1.0 
    
    Apply `request` modifications to `payload`.

    Return modified `payload` copy.
    '''
    from experimental.tools import requesttools
    from experimental.tools import settingtools
    from experimental.tools import symbolictimetools

    request_klasses = (
        requesttools.Request, 
        symbolictimetools.VoiceSelector,
        )

    payload_klasses = (
        list, tuple,
        rhythmmakertools.RhythmMaker,
        settingtools.OffsetPositionedExpression,
        )

    assert isinstance(request, request_klasses), repr(request)
    assert isinstance(payload, payload_klasses), repr(payload)
    assert hasattr(request, 'modifications')

    evaluation_context = {
        'Duration': durationtools.Duration,
        'RotationIndicator': settingtools.RotationIndicator,
        'request': request,
        'result': None,
        'sequencetools': sequencetools,
        }

    for modification in request.modifications:
        assert 'target' in modification
        target = copy.deepcopy(payload)
        evaluation_context['target'] = target
        exec(modification, evaluation_context)
        if evaluation_context['result'] is None:
            payload = target
        else:
            payload = evaluation_context['result']

    return payload 
