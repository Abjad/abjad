from abjad.tools import spannertools


def get_tie_spanner_attached_to_component(component):
    r'''.. versionadded:: 2.10

    Get the only tie spanner attached to `component`::

        >>> staff = Staff("c'8 ~ c'8 d'4")

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'8
            d'4
        }

    ::

        >>> tietools.get_tie_spanner_attached_to_component(staff[0])
        TieSpanner(c'8, c'8)

    Return tie spanner.

    Raise missing spanner error when no tie spanner attached to `component`.

    Raise extra spanner error when more than one tie spanner attached to `component`.
    '''
    from abjad.tools import tietools

    return spannertools.get_the_only_spanner_attached_to_component(component, tietools.TieSpanner)
