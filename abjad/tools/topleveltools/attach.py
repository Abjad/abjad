import types


def attach(attachable, component_expression, target_context=None):
    r'''Attaches `attachable` to `component_expression`.

    Creates attachment expression effective at `target_context`.

    Derives `target_context` from the default target context of `attachable`
    when `target_context` is none.

    Returns none.
    '''
    from abjad.tools import scoretools

    if target_context is not None:
        if isinstance(target_context, types.TypeType):
            assert issubclass(target_context, scoretools.Context)
        else:
            assert isinstance(target_context, scoretools.Context)
        attachable._target_context = target_context

    attachable._attach(component_expression)
