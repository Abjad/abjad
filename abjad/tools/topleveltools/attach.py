import types


def attach(indicator, component_expression, scope=None):
    r'''Attaches `indicator` to `component_expression`.

    Creates attachment expression effective at `scope`.

    Derives `scope` from the default target context of `indicator`
    when `scope` is none.

    Returns none.
    '''
    from abjad.tools import scoretools

    if scope is not None:
        assert hasattr(indicator, '_attach')
        assert hasattr(indicator, '_scope')
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context)
        else:
            assert isinstance(scope, scoretools.Context)
        indicator._scope = scope

    if hasattr(indicator, '_attach'):
        indicator._attach(component_expression)
    elif hasattr(component_expression, '_indicators'):
        component_expression._indicators.append(indicator)
    else:
        message = 'can not attach {!r} to {!r}.'
        message = message.format(indicator, component_expression)
        raise TypeError(message)
