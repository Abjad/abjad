from abjad.tools import formattools
from abjad.tools.containertools._format_container import _format_slot_1
from abjad.tools.containertools._format_container import _format_slot_4
from abjad.tools.containertools._format_container import _format_slot_6
from abjad.tools.containertools._format_container import _format_slot_7


def _format_context(context, pieces=False):
    result = []
    result.extend(_format_slot_1(context))
    result.extend(_format_slot_2(context))
    result.extend(_format_slot_3(context))
    result.extend(_format_slot_4(context))
    result.extend(_format_slot_5(context))
    result.extend(_format_slot_6(context))
    result.extend(_format_slot_7(context))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    if pieces:
        return contributions
    else:
        return '\n'.join(contributions)

def _format_slot_2(context):
    result = []
    if context.is_parallel:
        brackets_open = ['<<']
    else:
        brackets_open = ['{']
    engraver_removals = context._format_engraver_removals()
    engraver_consists = context._format_engraver_consists()
    overrides = formattools.get_grob_override_format_contributions(context)
    overrides = overrides[1]
    settings = formattools.get_context_setting_format_contributions(context)
    settings = settings[1]
    if engraver_removals or engraver_consists or overrides or settings:
        contributions = [context._format_invocation() + r' \with {']
        result.append([('context_brackets', 'open'), contributions])
        contributions = ['\t' + x for x in engraver_removals]
        result.append([('engraver removals', 'engraver_removals'), contributions])
        contributions = ['\t' + x for x in engraver_consists]
        result.append([('engraver consists', 'engraver_consists'), contributions])
        contributions = ['\t' + x for x in overrides]
        result.append([('overrides', 'overrides'), contributions])
        contributions = ['\t' + x for x in settings]
        result.append([('settings', 'settings'), contributions])
        contributions = ['} %s' % brackets_open[0]]
        result.append([('context_brackets', 'open'), contributions])
    else:
        contributions = [context._format_invocation() + ' %s' % brackets_open[0]]
        result.append([('context_brackets', 'open'), contributions])
    return tuple(result)

def _format_slot_3(context):
    result = []
    result.append(formattools.get_comment_format_contributions(context, 'opening'))
    result.append(formattools.get_context_mark_format_contributions(context, 'opening'))
    result.append(formattools.get_lilypond_command_mark_format_contributions(context, 'opening'))
    context._format_slot_contributions_with_indent(result)
    return tuple(result)

def _format_slot_5(context):
    result = []
    result.append(formattools.get_context_mark_format_contributions(context, 'closing'))
    result.append(formattools.get_lilypond_command_mark_format_contributions(context, 'closing'))
    result.append(formattools.get_comment_format_contributions(context, 'closing'))
    context._format_slot_contributions_with_indent(result)
    return tuple(result)
