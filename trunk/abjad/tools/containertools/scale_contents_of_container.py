# -*- encoding: utf-8 -*-
def scale_contents_of_container(container, multiplier):
    r'''Scale contents of `container` by dot `multiplier`:

    ::

        >>> staff = Staff("c'8 d'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        >>> containertools.scale_contents_of_container(staff, Multiplier(3, 2))
        Staff{2}

    ::

        >>> f(staff)
        \new Staff {
            c'8. [
            d'8. ]
        }

    Scale contents of `container` by tie `multiplier`:

    ::

        >>> staff = Staff("c'8 d'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        >>> containertools.scale_contents_of_container(staff, Multiplier(5, 4))
        Staff{4}

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ~
            c'32
            d'8 ~
            d'32 ]
        }

    Scale contents of `container` by `multiplier` without 
    power-of-two denominator:

    ::

        >>> staff = Staff("c'8 d'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        >>> containertools.scale_contents_of_container(staff, Multiplier(4, 3))
        Staff{2}

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'4 [
            }
            \times 2/3 {
                d'4 ]
            }
        }

    Return `container`.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import measuretools
    from abjad.tools import selectiontools
    from abjad.tools import tuplettools

    for expr in \
        iterationtools.iterate_topmost_tie_chains_and_components_in_expr(
        container[:]):
        if isinstance(expr, leaftools.TieChain):
            new_written_duration = multiplier * expr.written_duration
            expr._add_or_remove_notes_to_achieve_written_duration(
                new_written_duration)
        elif isinstance(expr, tuplettools.FixedDurationTuplet):
            selection = selectiontools.select_tuplets(expr)
            selection.scale_contents(multiplier)
        elif isinstance(expr, measuretools.Measure):
            measuretools.scale_contents_of_measures_in_expr(expr, multiplier)
        else:
            raise NotImplementedError(expr)

    return container
