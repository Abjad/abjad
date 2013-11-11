import types


def attach(item, component_expression, target_context=None):
    r'''Attaches `item` to `component_expression`.

    Creates attachment expression effective at `target_context`.

    Derives `target_context` from the default target context of `item`
    when `target_context` is none.

    Returns none.
    '''
    from abjad.tools import scoretools

    if target_context is not None:
        assert hasattr(item, '_attach')
        assert hasattr(item, '_target_context')
        if isinstance(target_context, types.TypeType):
            assert issubclass(target_context, scoretools.Context)
        else:
            assert isinstance(target_context, scoretools.Context)
        item._target_context = target_context

    if hasattr(item, '_attach'):
        item._attach(component_expression)
    elif hasattr(component_expression, '_attached_items'):
        from abjad.tools import durationtools
        assert type(item) == durationtools.Multiplier, repr(item)
        component_expression._attached_items.append(item)
    else:
        message = 'can not attach {!r} to {!r}'
        message = message.format(item, component_expression)
        raise TypeError(message)
