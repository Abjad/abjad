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

    component = component_expression
    assert isinstance(component, scoretools.Component), repr(component)

    if isinstance(indicator, indicatortools.IndicatorWrapper):
        scope = scope or indicator.scope
        indicator._detach()
        indicator = indicator.indicator
        assert hasattr(indicator, '_default_scope')

    if hasattr(indicator, '_default_scope'):
        scope = scope or indicator._default_scope
        assert scope is not None
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component,
            scope,
            )
        prototype = type(wrapper.indicator)
        effective = component._get_effective_indicator(prototype, unwrap=False)
        if effective is not None:
            indicator_start = effective.component._get_timespan().start_offset
            component_start = component._get_timespan().start_offset
            if indicator_start == component_start:
                message = 'effective indicator already attached.'
                raise ValueError(message)
        wrapper._bind_to_component(component)
        component._indicators.append(wrapper)
    else:
        assert scope is None
        component._indicators.append(indicator)
