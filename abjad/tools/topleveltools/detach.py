# -*- coding: utf-8 -*-


def detach(prototype, component_expression=None):
    r'''Detaches `prototype` indicators from `component_expression`.

    ..  container:: example

        Detaches articulations from first note in staff:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> attach(Articulation('>'), staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 -\accent
                d'4
                e'4
                f'4
            }

        ::

            >>> detach(Articulation, staff[0])
            (Articulation('>'),)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
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
    spanners = []
    grace_containers = []
    inspector = abjad.inspect_(component_expression)
    if isinstance(prototype, type):
        if issubclass(prototype, abjad.Spanner):
            spanners = inspector.get_spanners(prototype)
        elif issubclass(prototype, abjad.GraceContainer):
            grace_containers = inspector.get_grace_containers(prototype)
        else:
            assert hasattr(component_expression, '_indicator_expressions')
            result = []
            for item in component_expression._indicator_expressions[:]:
                if isinstance(item, prototype):
                    component_expression._indicator_expressions.remove(item)
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
        elif isinstance(prototype, abjad.GraceContainer):
            grace_containers = inspector.get_grace_containers(
                kind=prototype.kind,
                )
        else:
            assert hasattr(component_expression, '_indicator_expressions')
            result = []
            for item in component_expression._indicator_expressions[:]:
                if item == prototype:
                    component_expression._indicator_expressions.remove(item)
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
    items.extend(grace_containers)
    for item in items:
        item._detach()
    items = tuple(items)
    return items
