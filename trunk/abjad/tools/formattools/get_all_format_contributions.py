from abjad.tools.formattools.get_all_mark_format_contributions import get_all_mark_format_contributions
from abjad.tools.formattools.get_context_setting_format_contributions import get_context_setting_format_contributions
from abjad.tools.formattools.get_grob_override_format_contributions import get_grob_override_format_contributions
from abjad.tools.formattools.get_grob_revert_format_contributions import get_grob_revert_format_contributions
from abjad.tools.formattools.get_spanner_format_contributions import get_spanner_format_contributions


def get_all_format_contributions(component):
    '''Get all format contributions for `component` as a nested dictionary structure.

    Return dict.
    '''

    result = get_all_mark_format_contributions(component)

    for slot, contributions in get_spanner_format_contributions(component).iteritems():
        if slot not in result:
            result[slot] = { }
        result[slot]['spanners'] = contributions

    settings = get_context_setting_format_contributions(component)[1]
    if settings:
        result['context settings'] = settings

    overrides = get_grob_override_format_contributions(component)[1]
    if overrides:
        result['grob overrides'] = overrides
    
    reverts = get_grob_revert_format_contributions(component)[1]
    if reverts:
        result['grob reverts'] = reverts

    return result
