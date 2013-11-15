import types


def detach(indicator, component_expression):
    r'''Detaches all matching indicators from `component_expression`.

    Returns tuple of zero detached indicators.
    '''
    from abjad.tools import marktools
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools.agenttools.InspectionAgent import inspect

    marks, spanners, grace_containers = [], [], []
    inspector = inspect(component_expression)
    if isinstance(indicator, types.TypeType):
        if issubclass(indicator, marktools.ContextMark):
            marks = inspector.get_marks(indicator)
        elif issubclass(indicator, spannertools.Spanner):
            spanners = inspector.get_spanners(indicator)
        elif issubclass(indicator, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(indicator)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if isinstance(x, indicator):
                    component_expression._indicators.remove(x)
                    result.append(x)
            result = tuple(result)
            return result
    else:
        if isinstance(indicator, marktools.ContextMark):
            marks = inspector.get_marks(indicator)
        elif isinstance(indicator, spannertools.Spanner):
            spanners = inspector.get_spanners(indicator)
        elif isinstance(indicator, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(indicator)
        else:
            assert hasattr(component_expression, '_indicators')
            result = []
            for x in component_expression._indicators[:]:
                if x == indicator:
                    component_expression._indicators.remove(x)
                    result.append(x)
            result = tuple(result)
            return result
    indicators = []
    indicators.extend(marks)
    indicators.extend(spanners)
    indicators.extend(grace_containers)
    for indicator in indicators:
        indicator._detach()
    indicators = tuple(indicators)
    return indicators
