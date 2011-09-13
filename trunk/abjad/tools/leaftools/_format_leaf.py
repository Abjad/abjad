from abjad.tools.marktools._get_articulation_format_contributions import _get_articulation_format_contributions
from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
from abjad.tools.contexttools._get_context_mark_format_contributions_for_slot import _get_context_mark_format_contributions_for_slot
from abjad.tools.contexttools._get_context_setting_format_contributions import _get_context_setting_format_contributions
from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.markuptools._get_markup_format_contributions import _get_markup_format_contributions
from abjad.tools.spannertools._get_spanner_format_contributions_for_leaf_slot import _get_spanner_format_contributions_for_leaf_slot
from abjad.tools.marktools._get_stem_tremolo_format_contributions import _get_stem_tremolo_format_contributions
from abjad.tools import sequencetools


def _format_leaf(leaf):
    result = []
    result.extend(_get_slot_1(leaf))
    result.extend(_get_slot_3(leaf))
    result.extend(_get_slot_4(leaf))
    result.extend(_get_slot_5(leaf))
    result.extend(_get_slot_7(leaf))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    return '\n'.join(contributions)

def _report_leaf_format_contributors(leaf):
    report = ''
    report += 'slot 1:\n'
    report += _process_contribution_packet(_get_slot_1(leaf))
    report += 'slot 3:\n'
    report += _process_contribution_packet(_get_slot_3(leaf))
    report += 'slot 4:\n'
    report += '\tleaf body:\n'
    report += '\t\t' + _get_slot_4(leaf)[0][1][0] + '\n'
    report += 'slot 5:\n'
    report += _process_contribution_packet(_get_slot_5(leaf))
    report += 'slot 7:\n'
    report += _process_contribution_packet(_get_slot_7(leaf))
    return report

def _process_contribution_packet(contribution_packet):
    result = ''
    for contributor, contributions in contribution_packet:
        if contributions:
            if isinstance(contributor, tuple):
                contributor = '\t' + contributor[0] + ':\n'
            else:
                contributor = '\t' + contributor + ':\n'
            result += contributor
            for contribution in contributions:
                contribution = '\t\t' + contribution + '\n'
                result += contribution
    return result

def _get_agrace_body(leaf):
    result = []
    if hasattr(leaf, '_after_grace'):
        after_grace = leaf.after_grace
        if len(after_grace):
            result.append(after_grace.format)
    return ['agrace body', result]

def _get_agrace_opening(leaf):
    result = []
    if hasattr(leaf, '_after_grace'):
        if len(leaf.after_grace):
            result.append(r'\afterGrace')
    return ['agrace opening', result]

def _get_grace_body(leaf):
    result = []
    if hasattr(leaf, '_grace'):
        grace = leaf.grace
        if len(grace):
            result.append(grace.format)
    return ['grace body', result]

def _get_leaf_body(leaf):
    result = []
    client = leaf
    result.append(_get_nucleus(leaf))
    result.append(_get_stem_tremolo_format_contributions(leaf))
    result.append(_get_articulation_format_contributions(leaf))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'right'))
    result.append(_get_context_mark_format_contributions_for_slot(leaf, 'right'))
    result.append(_get_markup_format_contributions(client))
    result.append(_get_spanner_format_contributions_for_leaf_slot(client, 'right'))
    result.append(_get_comment_format_contributions_for_slot(client, 'right'))
    result = [x[1] for x in result]
    result = sequencetools.flatten_sequence(result)
    result = [' '.join(result)]
    return ['leaf body', result]

def _get_nucleus(leaf):
    from abjad.tools.chordtools.Chord import Chord
    if not isinstance(leaf, Chord):
        return ['nucleus', leaf._body]
    result =  []
    chord = leaf
    note_heads = chord.note_heads
    if any(['\n' in x.format for x in note_heads]):
        for note_head in note_heads:
            format = note_head.format
            format_list = format.split('\n')
            format_list = ['\t' + x for x in format_list]
            result.extend(format_list)
        result.insert(0, '<')
        result.append('>')
        result = '\n'.join(result)
        result += str(chord._formatted_duration)
    else:
        result.extend([x.format for x in note_heads])
        result = '<%s>%s' % (' '.join(result), chord._formatted_duration)
    # single string, but wrapped in list bc contribution
    return ['nucleus', [result]]

def _get_slot_1(leaf):
    result = []
    result.append(_get_grace_body(leaf))
    result.append(_get_comment_format_contributions_for_slot(leaf, 'before'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'before'))
    result.append(_get_context_mark_format_contributions_for_slot(leaf, 'before'))
    result.append(_get_grob_override_format_contributions(leaf))
    result.append(_get_context_setting_format_contributions(leaf))
    result.append(_get_spanner_format_contributions_for_leaf_slot(leaf, 'before'))
    return result

def _get_slot_3(leaf):
    result = []
    result.append(_get_comment_format_contributions_for_slot(leaf, 'opening'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'opening'))
    result.append(_get_context_mark_format_contributions_for_slot(leaf, 'opening'))
    result.append(_get_agrace_opening(leaf))
    return result

def _get_slot_4(leaf):
    result = []
    result.append(_get_leaf_body(leaf))
    return result

def _get_slot_5(leaf):
    result = []
    result.append(_get_agrace_body(leaf))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'closing'))
    result.append(_get_context_mark_format_contributions_for_slot(leaf, 'closing'))
    result.append(_get_comment_format_contributions_for_slot(leaf, 'closing'))
    return result

def _get_slot_7(leaf):
    result = []
    result.append(_get_spanner_format_contributions_for_leaf_slot(leaf, 'after'))
    result.append(_get_context_mark_format_contributions_for_slot(leaf, 'after'))
    result.append(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'after'))
    result.append(_get_comment_format_contributions_for_slot(leaf, 'after'))
    return result
