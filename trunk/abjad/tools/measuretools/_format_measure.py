from abjad.tools import formattools
from abjad.tools.containertools._format_container import _format_slot_1
from abjad.tools.containertools._format_container import _format_slot_2
from abjad.tools.containertools._format_container import _format_slot_4
from abjad.tools.containertools._format_container import _format_slot_5
from abjad.tools.containertools._format_container import _format_slot_6
from abjad.tools.containertools._format_container import _format_slot_7


def _format_measure(measure, pieces=False):
    result = []
    result.extend(_format_slot_1(measure))
    result.extend(_format_slot_2(measure))
    result.extend(_format_slot_3(measure))
    result.extend(_format_slot_4(measure))
    result.extend(_format_slot_5(measure))
    result.extend(_format_slot_6(measure))
    result.extend(_format_slot_7(measure))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    if pieces:
        return contributions
    else:
        return '\n'.join(contributions)
    
def _format_slot_3(measure):
        r'''This is the slot where LilyPond grob \override commands live.
        This is also the slot where LilyPond \time commands live.
        '''
        result = []
        result.append(formattools.get_comment_format_contributions(measure, 'opening'))
        result.append(formattools.get_grob_override_format_contributions(measure))
        result.append(formattools.get_context_setting_format_contributions(measure))
        result.append(formattools.get_context_mark_format_contributions(measure, 'opening'))
        measure._format_slot_contributions_with_indent(result)
        return tuple(result)
