# -*- coding: utf-8 -*-


def detach(prototype, component_expression=None):
    r'''Detaches from `component_expression` all items matching `prototype`.

    Returns tuple of zero or more detached items.
    '''
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools import topleveltools
    if isinstance(prototype, spannertools.Spanner):
        prototype._detach()
        return
    assert component_expression is not None
    spanners = []
    grace_containers = []
    inspector = topleveltools.inspect_(component_expression)
    if isinstance(prototype, type):
        if issubclass(prototype, spannertools.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif issubclass(prototype, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(prototype)
        else:
            assert hasattr(component_expression, '_indicator_expressions')
            result = []
            for x in component_expression._indicator_expressions[:]:
                if isinstance(x, prototype):
                    component_expression._indicator_expressions.remove(x)
                    result.append(x)
                # indicator is a expression
                elif (hasattr(x, 'indicator') and
                    isinstance(x.indicator, prototype)):
                    x._detach()
                    result.append(x.indicator)
            result = tuple(result)
            return result
    else:
        if isinstance(prototype, spannertools.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif isinstance(prototype, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(
                kind=prototype.kind,
                )
        else:
            assert hasattr(component_expression, '_indicator_expressions')
            result = []
            for x in component_expression._indicator_expressions[:]:
                if x == prototype:
                    component_expression._indicator_expressions.remove(x)
                    result.append(x)
                # indicator is an expression
                elif hasattr(x, 'indicator') and x.indicator == prototype:
                    x._detach()
                    result.append(x.indicator)
            result = tuple(result)
            return result
    items = []
    items.extend(spanners)
    items.extend(grace_containers)
    for item in items:
        item._detach()
    items = tuple(items)
    return items