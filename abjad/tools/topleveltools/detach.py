def detach(prototype, component_expression=None):
    r'''Detaches `prototype` indicators from `component_expression`.

    ..  container:: example

        Detaches articulations from first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('>'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4 -\accent
                d'4
                e'4
                f'4
            }

        >>> abjad.detach(abjad.Articulation, staff[0])
        (Articulation('>'),)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

    Returns tuple of zero or more detached items.
    '''
    import abjad
    if isinstance(prototype, abjad.Spanner):
        prototype._detach()
        return
    assert component_expression is not None
    after_grace_container = None
    grace_container = None
    spanners = []
    inspector = abjad.inspect(component_expression)
    if isinstance(prototype, type):
        if issubclass(prototype, abjad.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif issubclass(prototype, abjad.AfterGraceContainer):
            after_grace_container = inspector.get_after_grace_container()
        elif issubclass(prototype, abjad.GraceContainer):
            grace_container = inspector.get_grace_container()
        else:
            assert hasattr(component_expression, '_indicator_wrappers')
            result = []
            for item in component_expression._indicator_wrappers[:]:
                if isinstance(item, prototype):
                    component_expression._indicator_wrappers.remove(item)
                    result.append(item)
                # indicator is a expression
                elif (
                    hasattr(item, '_indicator') and
                    isinstance(item.indicator, prototype)
                    ):
                    item._detach()
                    result.append(item.indicator)
            result = tuple(result)
            return result
    else:
        if isinstance(prototype, abjad.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif isinstance(prototype, abjad.AfterGraceContainer):
            after_grace_container = inspector.get_after_grace_container()
        elif isinstance(prototype, abjad.GraceContainer):
            grace_container = inspector.get_grace_container()
        else:
            assert hasattr(component_expression, '_indicator_wrappers')
            result = []
            for item in component_expression._indicator_wrappers[:]:
                if item == prototype:
                    component_expression._indicator_wrappers.remove(item)
                    result.append(item)
                # indicator is an expression
                elif (
                    hasattr(item, '_indicator') and
                    item.indicator == prototype
                    ):
                    item._detach()
                    result.append(item.indicator)
            result = tuple(result)
            return result
    items = []
    items.extend(spanners)
    if after_grace_container is not None:
        items.append(after_grace_container)
    if grace_container is not None:
        items.append(grace_container)
    for item in items:
        item._detach()
    items = tuple(items)
    return items
