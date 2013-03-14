from abjad.tools import componenttools


def get_spanners_attached_to_any_improper_child_of_component(component, klass=None,
    set_spanner_format_contribution_state=False, clear_deposited_spanner_format_contributions=False):
    r'''.. versionadded:: 2.0

    Get all spanners attached to any improper children of `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
        >>> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
        >>> trill = spannertools.TrillSpanner(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8 )
            e'8 (
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> len(spannertools.get_spanners_attached_to_any_improper_child_of_component(staff))
        4

    Get all spanners of `klass` attached to any proper children of `component`::

        >>> spanner_klass = spannertools.SlurSpanner
        >>> result = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        ... staff, spanner_klass)

    ::

        >>> list(sorted(result))
        [SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)]

    Get all spanners of any `klass` attached to any proper children of `component`::

        >>> spanner_klasses = (spannertools.SlurSpanner, beamtools.BeamSpanner)
        >>> result = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        ... staff, spanner_klasses)

    ::

        >>> list(sorted(result))
        [BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)]

    Return unordered set of zero or more spanners.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    # initialize result set
    result = set([])

    # iterate proper children of component
    for child in iterationtools.iterate_components_in_expr([component]):
        result.update(spannertools.get_spanners_attached_to_component(child, klass))
        if set_spanner_format_contribution_state:
            child._spanner_format_contributions_are_current = True
        if clear_deposited_spanner_format_contributions:
            child._spanner_format_contributions = {}

    # return result
    return result
