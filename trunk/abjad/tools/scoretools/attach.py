def attach(attachable, component_expression):
    r'''Attaches `attachable` to `component_expression`.

    Returns attachable when attachable is a mark.

    Returns none when attachable is a spanner.
    '''

    return attachable.attach(component_expression)
