# -*- coding: utf-8 -*-


def attach(
    indicator,
    component_expression,
    scope=None,
    is_annotation=None,
    name=None,
    synthetic_offset=None,
    ):
    r'''Attaches `indicator` to `component_expression`.

    ..  container:: example

        Attaches clef to first note in staff:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> attach(Clef('alto'), staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Attaches accent to last two notes in staff:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> attach(Articulation('>'), staff[-2])
            >>> attach(Articulation('>'), staff[-1])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4 -\accent
                f'4 -\accent
            }

    Derives scope from the default scope of `indicator` when `scope` is none.

    Treats indicator as annotation when `is_annotation` is true.

    Returns none.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools.topleveltools import iterate

    if hasattr(indicator, '_attachment_test_all'):
        if not indicator._attachment_test_all(component_expression):
            message = '{!r} attachment test fails for {!r}.'
            message = message.format(indicator, component_expression)
            raise Exception(message)

    if hasattr(indicator, '_attach'):
        prototype = (spannertools.Spanner, scoretools.GraceContainer)
        assert isinstance(indicator, prototype), repr(indicator)
        assert scope is None
        if isinstance(indicator, spannertools.Spanner):
            name = name or indicator.name
            indicator._name = name
            leaves = []
            try:
                for x in component_expression:
                    if isinstance(x, scoretools.Leaf):
                        leaves.append(x)
                    else:
                        leaves.extend(iterate(x).by_leaf())
            except TypeError:
                leaves.append(component_expression)
            indicator._attach(leaves)
        else:
            indicator._attach(component_expression)
        return

    component = component_expression
    prototype = (scoretools.Component, spannertools.Spanner)
    if not isinstance(component, prototype):
        message = 'must be component or spanner: {!r}.'
        message = message.format(component)
        raise Exception(message)

    if isinstance(indicator, indicatortools.IndicatorExpression):
        is_annotation = is_annotation or indicator.is_annotation
        name = name or indicator.name
        scope = scope or indicator.scope
        synthetic_offset = synthetic_offset or indicator.synthetic_offset
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
        synthetic_offset=synthetic_offset,
        )
    expression._bind_to_component(component)
