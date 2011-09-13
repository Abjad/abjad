from abjad.exceptions import MissingSpannerError
from abjad.tools import componenttools
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner


def are_components_in_same_tie_spanner(components):
    '''True if all components in list share same tie spanner,
        otherwise False.

    .. versionchanged:: 2.0
        renamed ``tietools.are_in_same_spanner()`` to
        ``tietools.are_components_in_same_tie_spanner()``.
    '''

    assert componenttools.all_are_components(components)

    try:
        first = components[0]
        try:
            #first_tie_spanner = first.tie.spanner
            first_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
                first, TieSpanner)
            for component in components[1:]:
                #if component.tie.spanner is not first_tie_spanner:
                component_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
                    component, TieSpanner)
                if component_tie_spanner is not first_tie_spanner:
                    return False
        except MissingSpannerError:
            return False
    except IndexError:
        return True

    return True
