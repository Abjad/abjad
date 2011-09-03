def _report_container_modifications(container, output):
    r'''Read-only string representation of all parts of container format except container contents.
    '''

    from abjad.tools import containertools
    assert isinstance(container, containertools.Container)
    assert output in ('screen', 'string')

    result = []
    result.extend(container._formatter.slots.contributions('slot_1'))
    result.extend(container._formatter.slots.contributions('slot_2'))
    result.extend(container._formatter.slots.contributions('slot_3'))
    heart = '\t%%%%%% %s components omitted %%%%%%' % len(
        container._formatter.container)
    result.extend(['', heart, ''])
    result.extend(container._formatter.slots.contributions('slot_5'))
    result.extend(container._formatter.slots.contributions('slot_6'))
    result.extend(container._formatter.slots.contributions('slot_7'))
    result = '\n'.join(result)

    if output == 'screen':
        print result
    else:
        return result
