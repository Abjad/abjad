from abjad.tools.containertools._format_container import _get_slot_1
from abjad.tools.containertools._format_container import _get_slot_3
from abjad.tools.containertools._format_container import _get_slot_4
from abjad.tools.containertools._format_container import _get_slot_5
from abjad.tools.containertools._format_container import _get_slot_6
from abjad.tools.containertools._format_container import _get_slot_7


def _format_grace_container(grace_container, pieces=False):
    result = []
    result.extend(_get_slot_1(grace_container))
    result.extend(_get_slot_2(grace_container))
    result.extend(_get_slot_3(grace_container))
    result.extend(_get_slot_4(grace_container))
    result.extend(_get_slot_5(grace_container))
    result.extend(_get_slot_6(grace_container))
    result.extend(_get_slot_7(grace_container))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    if pieces:
        return contributions
    else:
        return '\n'.join(contributions)

def _get_slot_2(grace_container):
    result = []
    kind = grace_container.kind
    if kind == 'after':
        result.append([('grace_brackets', 'open'), ['{']])
    else:
        contributor = ('grace_brackets', 'open')
        contributions = [r'\%s {' % kind]
        result.append([contributor, contributions])
    return tuple(result)
