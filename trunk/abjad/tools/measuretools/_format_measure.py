from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.contexttools._get_context_mark_format_contributions_for_slot import \
    _get_context_mark_format_contributions_for_slot
from abjad.tools.contexttools._get_context_setting_format_contributions import \
    _get_context_setting_format_contributions
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
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
        result.append(_get_comment_format_contributions_for_slot(measure, 'opening'))
        result.append(_get_grob_override_format_contributions(measure))
        result.append(_get_context_setting_format_contributions(measure))
        result.append(_get_context_mark_format_contributions_for_slot(measure, 'opening'))
        measure._format_slot_contributions_with_indent(result)
        return tuple(result)
