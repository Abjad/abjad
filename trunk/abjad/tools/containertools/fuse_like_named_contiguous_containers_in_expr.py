from abjad.tools.containertools.Container import Container
from abjad.tools import componenttools


# TODO: change interface to fuse.containers_by_name() to pass containers-to-be-fused explicitly.
def fuse_like_named_contiguous_containers_in_expr(expr):
    r'''Fuse like-named contiguous containers in `expr`::

        abjad> staff = Staff(Voice("c'8 c'8") * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff.leaves)
        abjad> staff[0].name = 'soprano'
        abjad> staff[1].name = 'soprano'

    ::

        abjad> f(staff)
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

        abjad> containertools.fuse_like_named_contiguous_containers_in_expr(staff)
        Staff{1}

    ::

        abjad> f(staff)
        \new Staff {
            \context Voice = "soprano" {
                c'8
                d'8
                e'8
                f'8
            }
        }

    Return `expr`.

    .. versionchanged:: 2.0
        renamed ``fuse.containers_by_reference()`` to
        ``containertools.fuse_like_named_contiguous_containers_in_expr()``.
    '''
    from abjad.tools import containertools
    from abjad.tools.tuplettools.Tuplet import Tuplet

    merged = False
    if not isinstance(expr, list):
        expr = [expr]
    expr = Container(expr)

    g = componenttools.iterate_components_depth_first(expr, direction = 'right')
    for cmp in g:
        next = cmp._navigator._next_namesake
        if isinstance(next, Container) and not next.is_parallel and \
            not isinstance(next, Tuplet) and \
            componenttools.all_are_contiguous_components_in_same_score(
                [cmp, next], allow_orphans = True):
            cmp.extend(next)
            componenttools.remove_component_subtree_from_score_and_spanners([next])
            merged = True
    if merged:
        #print expr
        containertools.remove_empty_containers_in_expr(expr)
        return expr.pop(0)
    else:
        print 'debug did not merge'
        return None


# TODO implement containers_by_reference as a simple, non-recursive
# container fuser, like below:
#def fuse_like_named_contiguous_containers_in_expr(expr):
#   '''Fuse containers in self that are strictly contiguous
#      and that have the same name.'''
#
#   result = expr[0]
#   for cmp in expr[1:]:
#      if isinstance(cmp, Container) and not cmp.is_parallel:
#         componenttools.remove_component_subtree_from_score_and_spanners([cmp])
#         result.extend(cmp)
#   return result
