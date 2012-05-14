from abjad.tools.containertools._format_container import _format_slot_1
from abjad.tools.containertools._format_container import _format_slot_3
from abjad.tools.containertools._format_container import _format_slot_4
from abjad.tools.containertools._format_container import _format_slot_5
from abjad.tools.containertools._format_container import _format_slot_6
from abjad.tools.containertools._format_container import _format_slot_7


def _format_cluster(cluster, pieces=False):
    result = []
    result.extend(_format_slot_1(cluster))
    result.extend(_format_slot_2(cluster))
    result.extend(_format_slot_3(cluster))
    result.extend(_format_slot_4(cluster))
    result.extend(_format_slot_5(cluster))
    result.extend(_format_slot_6(cluster))
    result.extend(_format_slot_7(cluster))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    if pieces:
        return contributions
    else:
        return '\n'.join(contributions)

def _format_slot_2(cluster):
    result = []
    contributor = ('cluster_brackets', 'open')
    if cluster.is_parallel:
        brackets_open = ['<<']
    else:
        brackets_open = ['{']
    contributions = [r'\makeClusters %s' % brackets_open[0]]
    result.append([contributor, contributions])
    return tuple(result)
