import types


def attach(indicator, component_expression, scope=None):
    r'''Attaches `indicator` to `component_expression`.

    Derives scope from the default scope of `indicator` 
    when `scope` is none.

    Returns none.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools
    from abjad.tools import spannertools

    if hasattr(indicator, '_attach'):
        prototype = (spannertools.Spanner, scoretools.GraceContainer)
        assert isinstance(indicator, prototype), repr(indicator)
        assert scope is None
        indicator._attach(component_expression)
        return

    if isinstance(indicator, indicatortools.IndicatorWrapper):
        scope = scope or indicator.scope
        if isinstance(scope, types.TypeType):
            assert issubclass(scope, scoretools.Context), repr(scope)
        else:
            assert isinstance(scope, scoretools.Context), repr(scope)
        indicator._detach()
        indicator = indicator.indicator
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component_expression, 
            scope,
            )
        indicator = wrapper
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

    if isinstance(indicator, indicatortools.IndicatorWrapper):
        assert hasattr(indicator.indicator, '_default_scope')

    assert hasattr(component_expression, '_indicators')
    prototype = (type(indicator),)
    if isinstance(indicator, indicatortools.IndicatorWrapper):
        prototype = (type(indicator.indicator),)
    effective_indicator = component_expression._get_effective_indicator(
        prototype,
        unwrap=False,
        )
    if effective_indicator is not None:
        timespan = effective_indicator.component._get_timespan()
        mark_start_offset = timespan.start_offset
        timespan = component_expression._get_timespan()
        component_start_offset = timespan.start_offset
        if mark_start_offset == component_start_offset:
            message = 'effective indicator already attached'
            message += ' to some component starting at same time.'
            raise ValueError(message)
    if isinstance(indicator, indicatortools.IndicatorWrapper):
        indicator._bind_to_component(component_expression)
    component_expression._indicators.append(indicator)
