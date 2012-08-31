from abjad.tools import componenttools
from abjad.tools import spannertools


def are_components_in_same_tie_spanner(components):
    r'''True when `components` are in same tie spanner::

        >>> voice = Voice("c'8 ~ c' d' ~ d'")

    ::

        >>> f(voice)
        \new Voice {
            c'8 ~
            c'8
            d'8 ~
            d'8
        }

    ::

        >>> tietools.are_components_in_same_tie_spanner(voice[:2])
        True

    Otherwise false::

        >>> tietools.are_components_in_same_tie_spanner(voice[1:3])
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``tietools.are_in_same_spanner()`` to
        ``tietools.are_components_in_same_tie_spanner()``.
    '''
    from abjad.tools import tietools

    assert componenttools.all_are_components(components)

    try:
        first = components[0]
        try:
            first_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
                first, tietools.TieSpanner)
            for component in components[1:]:
                component_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
                    component, tietools.TieSpanner)
                if component_tie_spanner is not first_tie_spanner:
                    return False
        except MissingSpannerError:
            return False
    except IndexError:
        return True

    return True
