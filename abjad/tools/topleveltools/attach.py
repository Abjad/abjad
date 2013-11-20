import types


def attach(indicator, component_expression, scope=None):
    r'''Attaches `indicator` to `component_expression`.

    Derives `scope` from the default scope of `indicator` 
    when `scope` is none.

    Returns none.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools

    if isinstance(indicator, indicatortools.IndicatorWrapper):
        indicator._detach()
        scope = scope or indicator.scope
        wrapper = indicatortools.IndicatorWrapper(
            indicator.indicator, 
            component_expression, 
            scope,
            )
        indicator = wrapper
    elif scope is not None and hasattr(indicator, '_attach'):
        assert hasattr(indicator, 'scope')
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context)
        else:
            assert isinstance(scope, scoretools.Context)
        indicator._scope = scope
    elif scope is not None and not hasattr(indicator, '_attach'):
        scope = scope or indicator.scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component_expression, 
            scope,
            )
        indicator = wrapper
    elif not hasattr(indicator, '_attach') and hasattr(indicator, 'scope'):
        scope = scope or indicator.scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component_expression, 
            scope,
            )
        indicator = wrapper
    elif scope is None and hasattr(indicator, '_attach'):
        pass
    elif hasattr(indicator, '_default_scope'):
        scope = scope or indicator._default_scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component_expression, 
            scope,
            )
        indicator = wrapper

    if hasattr(indicator, '_attach'):
        indicator._attach(component_expression)
    elif hasattr(component_expression, '_indicators'):
        #print 'flamingo'
        if isinstance(indicator, indicatortools.IndicatorWrapper):
            classes = (type(indicator.indicator),)
        else:
            classes = (type(indicator),)
        #print classes, 'classes'
        effective_context_mark = \
            component_expression._get_effective_context_mark(
                classes,
                unwrap=False,
                )
        #print effective_context_mark, 'ECM'
        if effective_context_mark is not None:
            timespan = effective_context_mark._start_component._get_timespan()
            mark_start_offset = timespan.start_offset
            timespan = component_expression._get_timespan()
            start_component_start_offset = timespan.start_offset
            if mark_start_offset == start_component_start_offset:
                message = 'effective indicator already attached'
                message += ' to some component starting at same time.'
                raise ValueError(message)
        if isinstance(indicator, indicatortools.IndicatorWrapper):
            indicator._bind_to_start_component(component_expression)
        component_expression._indicators.append(indicator)
    else:
        message = 'can not attach {!r} to {!r}.'
        message = message.format(indicator, component_expression)
        raise TypeError(message)
