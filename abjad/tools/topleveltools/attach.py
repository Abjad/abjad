# -*- encoding: utf-8 -*-


def attach(
    indicator,
    component_expression,
    scope=None,
    is_annotation=None,
    name=None,
    ):
    r'''Attaches `indicator` to `component_expression`.

    Derives scope from the default scope of `indicator` when `scope` is none.

    Attached indicator is treated as annotative when `is_annotation` is true.

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
        if isinstance(indicator, spannertools.Spanner):
            name = name or indicator.name
            indicator._name = name
        return

    component = component_expression
    #assert isinstance(component, scoretools.Component), repr(component)
    prototype = (scoretools.Component, spannertools.Spanner)
    assert isinstance(component, prototype), repr(component)

    if isinstance(indicator, indicatortools.IndicatorExpression):
        is_annotation = is_annotation or indicator.is_annotation
        name = name or indicator.name
        scope = scope or indicator.scope
        indicator._detach()
        indicator = indicator.indicator

    if hasattr(indicator, '_default_scope'):
        scope = scope or indicator._default_scope

    expression = indicatortools.IndicatorExpression(
        component=component,
        indicator=indicator,
        is_annotation=is_annotation,
        name=name,
        scope=scope,
        )
    expression._bind_to_component(component)