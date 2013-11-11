import types


def detach(attachable, component_expression):
    r'''Detaches all matching attachables from `component_expression`.

    Returns tuple of zero detached attachables.
    '''
    from abjad.tools import marktools
    from abjad.tools import scoretools
    from abjad.tools import spannertools
    from abjad.tools.agenttools.InspectionAgent import inspect

    marks, spanners, grace_containers = [], [], []
    inspector = inspect(component_expression)
    if isinstance(attachable, types.TypeType):
        if issubclass(attachable, marktools.Mark):
            marks = inspector.get_marks(attachable)
        if issubclass(attachable, spannertools.Spanner):
            spanners = inspector.get_spanners(attachable)
        if issubclass(attachable, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(attachable)
#        else:
#            assert hasattr(component_expression, '_start_marks')
#            result = []
#            for x in component_expression._start_marks[:]:
#                if isinstance(x, attachable):
#                    component_expression._start_marks.remove(x)
#                    result.append(x)
#            result = tuple(result)
#            return result
    else:
        if isinstance(attachable, marktools.Mark):
            marks = inspector.get_marks(attachable)
        elif isinstance(attachable, spannertools.Spanner):
            spanners = inspector.get_spanners(attachable)
        elif isinstance(attachable, scoretools.GraceContainer):
            grace_containers = inspector.get_grace_containers(attachable)
    attachables = []
    attachables.extend(marks)
    attachables.extend(spanners)
    attachables.extend(grace_containers)
    for attachable in attachables:
        attachable._detach()
    attachables = tuple(attachables)
    return attachables
