import types


def detach(attachable, component_expression):
    r'''Detaches all matching attachables from `component_expression`.

    Returns tuple of zero detached attachables.
    '''
    from abjad.tools import marktools
    from abjad.tools import spannertools
    from abjad.tools.agenttools.InspectionAgent import inspect

    marks, spanners = [], []
    inspector = inspect(component_expression)
    if isinstance(attachable, types.TypeType):
        if issubclass(attachable, marktools.Mark):
            marks = inspector.get_marks(attachable)
        if issubclass(attachable, spannertools.Spanner):
            spanners = inspector.get_spanners(attachable)
    else:
        if isinstance(attachable, marktools.Mark):
            marks = inspector.get_marks(attachable)
        elif isinstance(attachable, spannertools.Spanner):
            spanners = inspector.get_spanners(attachable)
    attachables = []
    attachables.extend(marks)
    attachables.extend(spanners)
    for attachable in attachables:
        attachable._detach()
    attachables = tuple(attachables)
    return attachables
