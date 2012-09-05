from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import schemetools
from abjad.tools import spannertools
from abjad.tools import voicetools


def make_voice_from_nonoverlapping_intervals(intervals, colorkey=None, pitch=None):

    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return voicetools.Voice([])
    assert timeintervaltools.all_intervals_are_nonoverlapping(tree)

    voice = voicetools.Voice([])

    depth_tree = timeintervaltools.compute_depth_of_intervals_in_interval(tree, timeintervaltools.TimeInterval(0, tree.stop))

    if pitch is None:
        pitch = 0

    for i, depth_interval in enumerate(depth_tree):
        if depth_interval['depth'] == 0:
            if i == 0:
                rest = resttools.Rest(1)
                rest.duration_multiplier = depth_interval.duration
                voice.append(rest)
            else:
                note = notetools.Note(pitch, 1)
                note.duration_multiplier = depth_interval.duration
                note.override.note_head.transparent = True
                voice.append(note)
                spannertools.GlissandoSpanner(voice[-2:])
#                note = notetools.Note(0, 1)
#                note.duration_multiplier = 0
#                note.override.note_head.transparent = True
#                voice.append(note)
#                spannertools.GlissandoSpanner(voice[-2:])
#                rest = resttools.Rest(1)
#                rest.duration_multiplier = depth_interval.duration
#                voice.append(rest)

        elif depth_interval['depth'] == 1:
            note = notetools.Note(pitch, 1)
            note.duration_multiplier = depth_interval.duration
            if colorkey is not None:
                try:
                    original_interval = tree.find_intervals_starting_at_offset(depth_interval.start)[0]
                    color = schemetools.SchemeColor(original_interval[colorkey])
                    note.override.note_head.color = color
                    note.override.glissando.color = color
                except KeyError:
                    pass
            voice.append(note)
            if i != 0 and 0 < depth_tree[i - 1]['depth']:
                spannertools.GlissandoSpanner(voice[-2:])
            if depth_interval == depth_tree[-1]:
                note = notetools.Note(pitch, 1)
                note.override.note_head.transparent = True
                voice.append(note)
                spannertools.GlissandoSpanner(voice[-2:])

        else:
            raise Exception('Intervals were not non-overlapping!')

    voice.engraver_removals.append('Forbid_line_break_engraver')

    return voice
