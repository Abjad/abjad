import types


def detach(item, component_expression):
    r'''Detaches all matching items from `component_expression`.

    Returns tuple of zero detached items.
    '''
    from abjad.tools import marktools
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools.agenttools.InspectionAgent import inspect

    marks, spanners, grace_containers = [], [], []
    inspector = inspect(component_expression)
    if isinstance(item, types.TypeType):
        if issubclass(item, marktools.Mark):
            marks = inspector.get_marks(item)
        elif issubclass(item, spannertools.Spanner):
            spanners = inspector.get_spanners(item)
        elif issubclass(item, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(item)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if isinstance(x, item):
                    component_expression._indicators.remove(x)
                    result.append(x)
            result = tuple(result)
            return result
    else:
        if isinstance(item, marktools.Mark):
            marks = inspector.get_marks(item)
        elif isinstance(item, spannertools.Spanner):
            spanners = inspector.get_spanners(item)
        elif isinstance(item, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(item)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if x == item:
                    component_expression._indicators.remove(x)
                    result.append(x)
            result = tuple(result)
            return result
    items = []
    items.extend(marks)
    items.extend(spanners)
    items.extend(grace_containers)
    for item in items:
        item._detach()
    items = tuple(items)
    return items
