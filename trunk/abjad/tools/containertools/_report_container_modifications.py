def _report_container_modifications(container, output='string'):
    r'''String representation of all parts of container format except container contents.

    Return string.
    '''

    from abjad.tools import formattools
    from abjad.tools import containertools
    assert isinstance(container, containertools.Container)
    assert output in ('screen', 'string')

    fc = formattools.get_all_format_contributions(container)

    result = []

    result.extend(container._get_format_contributions_for_slot('before', fc))
    result.extend(container._get_format_contributions_for_slot('open brackets', fc))
    result.extend(container._get_format_contributions_for_slot('opening', fc))
    result.append('\t%%%%%% %s components omitted %%%%%%' % len(container))
    result.extend(container._get_format_contributions_for_slot('closing', fc))
    result.extend(container._get_format_contributions_for_slot('close brackets', fc))
    result.extend(container._get_format_contributions_for_slot('after', fc))

    result = '\n'.join(result)

    if output == 'screen':
        print result
    else:
        return result
