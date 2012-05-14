from abjad.tools import formattools
from abjad.tools import sequencetools


# TODO: move to bound leaf method
def _format_leaf(leaf):
    result = []
    result.extend(_format_slot_1(leaf))
    result.extend(_format_slot_3(leaf))
    result.extend(_format_slot_4(leaf))
    result.extend(_format_slot_5(leaf))
    result.extend(_format_slot_7(leaf))
    contributions = []
    for contributor, contribution in result:
        contributions.extend(contribution)
    return '\n'.join(contributions)

# TODO: move to bound leaf method
def _format_agrace_body(leaf):
    result = []
    if hasattr(leaf, '_after_grace'):
        after_grace = leaf.after_grace
        if len(after_grace):
            result.append(after_grace.format)
    return ['agrace body', result]

# TODO: move to bound leaf method
def _format_agrace_opening(leaf):
    result = []
    if hasattr(leaf, '_after_grace'):
        if len(leaf.after_grace):
            result.append(r'\afterGrace')
    return ['agrace opening', result]

# TODO: move to bound leaf method
def _format_grace_body(leaf):
    result = []
    if hasattr(leaf, '_grace'):
        grace = leaf.grace
        if len(grace):
            result.append(grace.format)
    return ['grace body', result]

# TODO: move to bound leaf method
def _format_leaf_body(leaf):
    result = []
    client = leaf
    result.append(_format_leaf_nucleus(leaf))
    result.append(formattools.get_stem_tremolo_format_contributions(leaf))
    result.append(formattools.get_articulation_format_contributions(leaf))
    result.append(formattools.get_lilypond_command_mark_format_contributions(leaf, 'right'))
    result.append(formattools.get_context_mark_format_contributions(leaf, 'right'))
    result.append(formattools.get_markup_format_contributions(client))
    result.append(formattools.get_spanner_format_contributions_for_leaf_slot(client, 'right'))
    result.append(formattools.get_comment_format_contributions(client, 'right'))
    result = [x[1] for x in result]
    result = sequencetools.flatten_sequence(result)
    result = [' '.join(result)]
    return ['leaf body', result]

# TODO: move to bound leaf method
def _format_leaf_nucleus(leaf):
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

# TODO: move to bound leaf method
def _format_slot_1(leaf):
    result = []
    result.append(_format_grace_body(leaf))
    result.append(formattools.get_comment_format_contributions(leaf, 'before'))
    result.append(formattools.get_lilypond_command_mark_format_contributions(leaf, 'before'))
    result.append(formattools.get_context_mark_format_contributions(leaf, 'before'))
    result.append(formattools.get_grob_override_format_contributions(leaf))
    result.append(formattools.get_context_setting_format_contributions(leaf))
    result.append(formattools.get_spanner_format_contributions_for_leaf_slot(leaf, 'before'))
    return result

# TODO: move to bound leaf method
def _format_slot_3(leaf):
    result = []
    result.append(formattools.get_comment_format_contributions(leaf, 'opening'))
    result.append(formattools.get_lilypond_command_mark_format_contributions(leaf, 'opening'))
    result.append(formattools.get_context_mark_format_contributions(leaf, 'opening'))
    result.append(_format_agrace_opening(leaf))
    return result

# TODO: move to bound leaf method
def _format_slot_4(leaf):
    result = []
    result.append(_format_leaf_body(leaf))
    return result

# TODO: move to bound leaf method
def _format_slot_5(leaf):
    result = []
    result.append(_format_agrace_body(leaf))
    result.append(formattools.get_lilypond_command_mark_format_contributions(leaf, 'closing'))
    result.append(formattools.get_context_mark_format_contributions(leaf, 'closing'))
    result.append(formattools.get_comment_format_contributions(leaf, 'closing'))
    return result

# TODO: move to bound leaf method
def _format_slot_7(leaf):
    result = []
    result.append(formattools.get_spanner_format_contributions_for_leaf_slot(leaf, 'after'))
    result.append(formattools.get_context_mark_format_contributions(leaf, 'after'))
    result.append(formattools.get_lilypond_command_mark_format_contributions(leaf, 'after'))
    result.append(formattools.get_comment_format_contributions(leaf, 'after'))
    return result
