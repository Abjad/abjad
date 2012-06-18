def expr_to_component_name(expr):
    r'''.. versionadded:: 1.0
    
    Change component to component name::

        >>> from experimental import specificationtools

    ::

        >>> voice = Voice("c'8 d'8 e'8 f'8", name='Voice 1')

    ::

        >>> specificationtools.expr_to_component_name(voice)
        'Voice 1'

    ::

    Leave string unchanged::

        >>> specificationtools.expr_to_component_name('Voice 1')
        'Voice 1'

    Raise exception on noncomponent, nonstring input.

    Return string.
    '''
    from abjad.tools import componenttools
    if isinstance(expr, componenttools.Component):
        return expr.name
    elif isinstance(expr, str):
        return expr
    else:
        raise Exception('{!r} is neither component nor string.'.format(expr))
