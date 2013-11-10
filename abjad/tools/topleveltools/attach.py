def attach(attachable, component_expression, target_context=None):
    r'''Attaches `attachable` to `component_expression`.

    Creates attachment expression effective at `target_context`.

    Derives `target_context` from the default target context of `attachable`
    when `target_context` is none.

    Returns none.
    '''

    attachable._attach(component_expression)
