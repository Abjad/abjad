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

    if hasattr(indicator, '_default_scope'):
        scope = scope or indicator._default_scope
        assert scope is not None
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component,
            scope,
            )
        wrapper._bind_to_component(component)
    else:
        assert scope is None
        wrapper = indicatortools.IndicatorWrapper(
            indicator, 
            component,
            scope,
            )
        wrapper._bind_to_component(component)
