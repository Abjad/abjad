def get_all_format_contributions(component):
    '''Get all format contributions for `component`.

    Return nested dictionary.
    '''
    from abjad.tools import formattools

    result = formattools.get_all_mark_format_contributions(component)

    for slot, contributions in formattools.get_spanner_format_contributions(component).iteritems():
        if slot not in result:
            result[slot] = {}
        result[slot]['spanners'] = contributions

    settings = formattools.get_context_setting_format_contributions(component)[1]
    if settings:
        result['context settings'] = settings

    overrides = formattools.get_grob_override_format_contributions(component)[1]
    if overrides:
        result['grob overrides'] = overrides

    reverts = formattools.get_grob_revert_format_contributions(component)[1]
    if reverts:
        result['grob reverts'] = reverts

    return result
