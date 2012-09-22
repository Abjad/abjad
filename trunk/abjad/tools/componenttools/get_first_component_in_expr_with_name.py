def get_first_component_in_expr_with_name(expr, name):
    '''.. versionadded:: 1.1

    Get first component in `expr` with `name`::

        >>> flute_staff = Staff("c'8 d'8 e'8 f'8")
        >>> flute_staff.name = 'Flute'
        >>> violin_staff = Staff("c'8 d'8 e'8 f'8")
        >>> violin_staff.name = 'Violin'
        >>> staff_group = scoretools.StaffGroup([flute_staff, violin_staff])
        >>> score = Score([staff_group])

    ::

        >>> componenttools.get_first_component_in_expr_with_name(score, 'Violin')
        Staff-"Violin"{4}

    .. versionchanged:: 2.0
        Function returns first component found.
        Function previously returned tuple of all components found.

    .. versionchanged:: 2.0
        renamed ``scoretools.find()`` to
        ``componenttools.get_first_component_in_expr_with_name()``.

    .. versionchanged:: 2.0
        Removed `klass` and `context` keywords.
        Function operates only on component name.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools

    if not isinstance(expr, (componenttools.Component, list, tuple)):
        raise TypeError('must be tuple, list or Abjad comonent.')

    for component in iterationtools.iterate_components_in_expr(expr):
        if name is None or getattr(component, 'name', None) == name:
            return component

    raise MissingComponentError
