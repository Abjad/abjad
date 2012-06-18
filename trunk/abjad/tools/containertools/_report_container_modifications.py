def _report_container_modifications(container, output='string'):
    r'''String representation of all parts of container format except container contents.

    Return string.
    '''

    from abjad.tools import containertools
    assert isinstance(container, containertools.Container)
    assert output in ('screen', 'string')

    result = []
    result.extend(container._get_format_contributions_for_slot('before'))
    result.extend(container._get_format_contributions_for_slot('open_brackets'))
    result.extend(container._get_format_contributions_for_slot('opening'))
    heart = '\t%%%%%% %s components omitted %%%%%%' % len(container)
    result.extend([heart])
    result.extend(container._get_format_contributions_for_slot('closing'))
    result.extend(container._get_format_contributions_for_slot('close_brackets'))
    result.extend(container._get_format_contributions_for_slot('after'))
    result = '\n'.join(result)

    if output == 'screen':
        print result
    else:
        return result
