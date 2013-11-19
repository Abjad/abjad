import types


def attach(indicator, component_expression, scope=None):
    r'''Attaches `indicator` to `component_expression`.

    Derives `scope` from the default scope of `indicator` 
    when `scope` is none.

    Returns none.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools

    if scope is not None and hasattr(indicator, '_attach'):
        assert hasattr(indicator, 'scope')
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context)
        else:
            assert isinstance(scope, scoretools.Context)
        indicator._scope = scope
    elif scope is not None and not hasattr(indicator, '_attach'):
        assert hasattr(indicator, 'scope')
        scope = scope or indicator.scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(indicator, scope)
        indicator = wrapper
    elif not hasattr(indicator, '_attach') and hasattr(indicator, 'scope'):
        scope = scope or indicator.scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(indicator, scope)
        indicator = wrapper
    elif scope is None and hasattr(indicator, '_attach'):
        pass
    elif hasattr(indicator, '_default_scope'):
        scope = scope or indicator._default_scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(indicator, scope)
        indicator = wrapper

    if hasattr(indicator, '_attach'):
        indicator._attach(component_expression)
    elif hasattr(component_expression, '_indicators'):
        component_expression._indicators.append(indicator)
    else:
        message = 'can not attach {!r} to {!r}.'
        message = message.format(indicator, component_expression)
        raise TypeError(message)
