from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.contexttools._get_context_setting_format_contributions import \
    _get_context_setting_format_contributions
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import \
    _get_grob_revert_format_contributions
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot


def _format_container(container):
    result = []
    result.extend(_format_slot_1(container))
    result.extend(_format_slot_2(container))
    result.extend(_format_slot_3(container))
    result.extend(_format_slot_4(container))
    result.extend(_format_slot_5(container))
    result.extend(_format_slot_6(container))
    result.extend(_format_slot_7(container))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    return '\n'.join(contributions)

def _format_slot_1(container):
    result = []
    result.append(_get_comment_format_contributions_for_slot(container, 'before'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'before'))
    return tuple(result)

def _format_slot_2(container):
    result = []
    if container.is_parallel:
        brackets_open = ['<<']
    else:
        brackets_open = ['{']
    result.append([('open brackets', ''), brackets_open])
    return tuple(result)

def _format_slot_3(container):
    result = []
    result.append(_get_comment_format_contributions_for_slot(container, 'opening'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'opening'))
    result.append(_get_grob_override_format_contributions(container))
    result.append(_get_context_setting_format_contributions(container))
    container._format_slot_contributions_with_indent(result)
    return tuple(result)

def _format_slot_4(container):
    result = []
    result.append([('contents', '_contents'), container._format_content_pieces()])
    return tuple(result)

def _format_slot_5(container):
    result = []
    result.append(_get_grob_revert_format_contributions(container))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'closing'))
    result.append(_get_comment_format_contributions_for_slot(container, 'closing'))
    container._format_slot_contributions_with_indent(result)
    return tuple(result)

def _format_slot_6(container):
    result = []
    if container.is_parallel:
        brackets_close = ['>>']
    else:
        brackets_close = ['}']
    result.append([('close brackets', ''), brackets_close])
    return tuple(result)

def _format_slot_7(container):
    result = []
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'after'))
    result.append(_get_comment_format_contributions_for_slot(container, 'after'))
    return tuple(result)
