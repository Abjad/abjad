def _report_container_modifications(container, output='string'):
    r'''String representation of all parts of container format except container contents.

    Return string.
    '''

    from abjad.tools import containertools
    assert isinstance(container, containertools.Container)
    assert output in ('screen', 'string')

    result = []
    result.extend(container._get_format_contributions_for_slot(1))
    result.extend(container._get_format_contributions_for_slot(2))
    result.extend(container._get_format_contributions_for_slot(3))
    heart = '\t%%%%%% %s components omitted %%%%%%' % len(container)
    result.extend([heart])
    result.extend(container._get_format_contributions_for_slot(5))
    result.extend(container._get_format_contributions_for_slot(6))
    result.extend(container._get_format_contributions_for_slot(7))
    result = '\n'.join(result)

    if output == 'screen':
        print result
    else:
        return result
