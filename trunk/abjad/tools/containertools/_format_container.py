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
    result.extend(_get_slot_1(container))
    result.extend(_get_slot_2(container))
    result.extend(_get_slot_3(container))
    result.extend(_get_slot_4(container))
    result.extend(_get_slot_5(container))
    result.extend(_get_slot_6(container))
    result.extend(_get_slot_7(container))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    return '\n'.join(contributions)

def _wrap(self, contributor, attr):
    '''Wrap format contribution with format source.'''
    if False:
        pass
    else:
        return [(contributor, attr), getattr(contributor, attr)]

def _get_slot_1(container):
    result = []
    result.append(_get_comment_format_contributions_for_slot(container, 'before'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'before'))
    return tuple(result)

def _get_slot_2(container):
    result = []
    if container.is_parallel:
        brackets_open = ['<<']
    else:
        brackets_open = ['{']
    result.append([('open brackets', ''), brackets_open])
    return tuple(result)

def _get_slot_3(container):
    result = []
    result.append(_get_comment_format_contributions_for_slot(container, 'opening'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'opening'))
    result.append(_get_grob_override_format_contributions(container))
    result.append(_get_context_setting_format_contributions(container))
    container._format_slot_contributions_with_indent(result)
    return tuple(result)

def _get_contents(container):
    '''Read-only list of tabbed lines of content.
    '''
    result = []
    for m in container._music:
        result.extend(m.format.split('\n'))
    result = ['\t' + x for x in result]
    return result

def _get_slot_4(container):
    result = []
    #result.append(self.wrap(self.formatter, '_contents'))
    result.append([('contents', '_contents'), _get_contents(container)]) # check this line
    return tuple(result)

def _get_slot_5(container):
    result = []
    result.append(_get_grob_revert_format_contributions(container))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'closing'))
    result.append(_get_comment_format_contributions_for_slot(container, 'closing'))
    container._format_slot_contributions_with_indent(result)
    return tuple(result)

def _get_slot_6(container):
    result = []
    if container.is_parallel:
        brackets_close = ['>>']
    else:
        brackets_close = ['}']
    result.append([('close brackets', ''), brackets_close])
    return tuple(result)

def _get_slot_7(container):
    result = []
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'after'))
    result.append(_get_comment_format_contributions_for_slot(container, 'after'))
    return tuple(result)
