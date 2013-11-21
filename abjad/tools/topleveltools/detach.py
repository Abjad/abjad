import types


def detach(prototype, component_expression):
    r'''Detaches from `component_expression` all items matching `prototype`.

    Returns tuple of zero or more detached items.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools.agenttools.InspectionAgent import inspect

    spanners = []
    grace_containers = []
    inspector = inspect(component_expression)
    if isinstance(prototype, types.TypeType):
        if issubclass(prototype, spannertools.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif issubclass(prototype, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(prototype)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if isinstance(x, prototype):
                    component_expression._indicators.remove(x)
                    result.append(x)
                # indicator is a wrapper
                elif hasattr(x, 'indicator') and \
                    isinstance(x.indicator, prototype):
                    x._detach()
                    result.append(x.indicator)
            result = tuple(result)
            return result
    else:
        if isinstance(prototype, spannertools.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif isinstance(prototype, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(prototype)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if x == prototype:
                    component_expression._indicators.remove(x)
                    result.append(x)
                # indicator is a wrapper
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
