from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import tietools


def scale_contents_of_container(container, multiplier):
    r'''.. versionadded:: 1.1

    Scale contents of `container` by dot `multiplier`::

        abjad> staff = Staff("c'8 d'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        abjad> containertools.scale_contents_of_container(staff, Duration(3, 2))
        Staff{2}

    ::

        abjad> f(staff)
        \new Staff {
            c'8. [
            d'8. ]
        }

    Scale contents of `container` by tie `multiplier`::

        abjad> staff = Staff("c'8 d'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        abjad> containertools.scale_contents_of_container(staff, Duration(5, 4))
        Staff{4}

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ~
            c'32
            d'8 ~
            d'32 ]
        }

    Scale contents of `container` by nonbinary `multiplier`::

        abjad> staff = Staff("c'8 d'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        abjad> containertools.scale_contents_of_container(staff, Duration(4, 3))
        Staff{2}

    ::

        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'4 [
            }
            \times 2/3 {
                d'4 ]
            }
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_scale()`` to
        ``containertools.scale_contents_of_container()``.
    '''
    from abjad.tools import tuplettools
    from abjad.tools.measuretools.Measure import Measure

    for expr in tietools.iterate_topmost_tie_chains_and_components_forward_in_expr(container[:]):
        if tietools.is_tie_chain(expr):
            tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(expr, multiplier)
        elif isinstance(expr, tuplettools.FixedDurationTuplet):
            tuplettools.scale_contents_of_tuplets_in_expr_by_multiplier(expr, multiplier)
        elif isinstance(expr, Measure):
            # TODO: Move import to higher level of scope? #
            from abjad.tools import measuretools
            measuretools.scale_contents_of_measures_in_expr(expr, multiplier)
        else:
            raise Exception(NotImplemented)

    return container
