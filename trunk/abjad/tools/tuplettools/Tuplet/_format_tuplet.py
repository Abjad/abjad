from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import \
    _get_grob_revert_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import \
    _get_grob_revert_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import \
    _get_grob_revert_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.marktools._get_comment_format_contributions_for_slot import \
    _get_comment_format_contributions_for_slot
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import \
    _get_grob_override_format_contributions
from abjad.tools.lilypondproxytools.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import \
    _get_grob_revert_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import \
    _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.containertools._format_container import _get_slot_4


def _format_tuplet(tuplet):
    result = []
    result.extend(_get_slot_1(tuplet))
    result.extend(_get_slot_2(tuplet))
    result.extend(_get_slot_3(tuplet))
    result.extend(_get_slot_4(tuplet))
    result.extend(_get_slot_5(tuplet))
    result.extend(_get_slot_6(tuplet))
    result.extend(_get_slot_7(tuplet))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    return '\n'.join(contributions)

def _get_slot_1(tuplet):
    result = []
    result.append(_get_comment_format_contributions_for_slot(tuplet, 'before'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'before'))
    result.append(_get_grob_override_format_contributions(tuplet))
    return tuple(result)

def _get_slot_2(tuplet):
    result = []
    if tuplet.multiplier:
        if tuplet.is_invisible:
            multiplier = tuplet.multiplier
            n, d = multiplier.numerator, multiplier.denominator
            contributor = (tuplet, 'is_invisible')
            contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
            result.append([contributor, contributions])
        else:
            contributor = ('tuplet_brackets', 'open')
            if tuplet.multiplier != 1:
                contributions = [r'%s\times %s %s' % (
                    tuplet._format_lilypond_fraction_command_string(),
                    tuplet._multiplier_fraction_string,
                    '{'
                    )]
            else:
                contributions = ['{']
            result.append([contributor, contributions])
    return tuple(result)

def _get_slot_3(tuplet):
    '''Read-only tuple of format contributions to appear immediately after tuplet opening.
    '''
    result = []
    result.append(_get_comment_format_contributions_for_slot(tuplet, 'opening'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'opening'))
    tuplet._format_slot_contributions_with_indent(result)
    return tuple(result)

def _get_slot_5(tuplet):
    '''Read-only tuple of format contributions to appear immediately before tuplet closing.
    '''
    result = []
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'closing'))
    result.append(_get_comment_format_contributions_for_slot(tuplet, 'closing'))
    tuplet._format_slot_contributions_with_indent(result)
    return tuple(result)

def _get_slot_6(tuplet):
    '''Read-only tuple of format contributions used to generate tuplet closing.
    '''
    result = []
    if tuplet.multiplier:
        result.append([('tuplet_brackets', 'close'), '}'])
    return tuple(result)

def _get_slot_7(tuplet):
    '''Read-only tuple of format contributions to appear immediately after tuplet closing.
    '''
    result = []
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'after'))
    result.append(_get_grob_revert_format_contributions(tuplet))
    result.append(_get_comment_format_contributions_for_slot(tuplet, 'after'))
    return tuple(result)
