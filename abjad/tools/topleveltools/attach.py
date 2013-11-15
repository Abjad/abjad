import types


def attach(item, component_expression, scope=None):
    r'''Attaches `item` to `component_expression`.

    Creates attachment expression effective at `scope`.

    Derives `scope` from the default target context of `item`
    when `scope` is none.

    Returns none.
    '''
    from abjad.tools import scoretools

    if scope is not None:
        assert hasattr(item, '_attach')
        assert hasattr(item, '_scope')
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context)
        else:
            assert isinstance(scope, scoretools.Context)
        item._scope = scope

    if hasattr(item, '_attach'):
        item._attach(component_expression)
    elif hasattr(component_expression, '_indicators'):
        component_expression._indicators.append(item)
    else:
        message = 'can not attach {!r} to {!r}.'
        message = message.format(item, component_expression)
        raise TypeError(message)
