# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


# TODO: change interface to fuse.containers_by_name() to pass containers-to-be-fused explicitly.
def fuse_like_named_contiguous_containers_in_expr(expr):
    r'''Fuse like-named contiguous containers in `expr`:

    ::

        >>> staff = Staff(r"\new Voice { c'8 d'8 } \new Voice { e'8 f'8 }")
        >>> staff[0].name = 'soprano'
        >>> staff[1].name = 'soprano'

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \context Voice = "soprano" {
                c'8
                d'8
            }
            \context Voice = "soprano" {
                e'8
                f'8
            }
        }

    ::

        >>> containertools.fuse_like_named_contiguous_containers_in_expr(staff)
        Staff{1}

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \context Voice = "soprano" {
                c'8
                d'8
                e'8
                f'8
            }
        }

    Return `expr`.
    '''
    from abjad.tools import containertools
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    merged = False
    if not isinstance(expr, list):
        expr = [expr]
    expr = containertools.Container(expr)

    g = iterationtools.iterate_components_depth_first(expr, direction=Right)
    for component in g:
        next_component = component._get_namesake(1)
        if isinstance(next_component, containertools.Container) and \
            not next_component.is_parallel and \
            not isinstance(next_component, tuplettools.Tuplet) and \
            component.select_parentage().root is \
                next_component.select_parentage().root:
                component.extend(next_component)
                componenttools.remove_component_subtree_from_score_and_spanners(
                    [next_component])
                merged = True
    if merged:
        #containertools.remove_leafless_containers_in_expr(expr)
        for container in iterationtools.iterate_containers_in_expr(expr):
            if not container.select_leaves():
                componenttools.remove_component_subtree_from_score_and_spanners(
                    [container])
        return expr.pop(0)
