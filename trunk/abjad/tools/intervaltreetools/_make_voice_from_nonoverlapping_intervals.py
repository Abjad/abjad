from abjad import Note
from abjad import Rest
from abjad import Voice
from abjad.tools.schemetools import SchemeColor
from abjad.tools.spannertools import GlissandoSpanner
from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.all_intervals_are_nonoverlapping import all_intervals_are_nonoverlapping
from abjad.tools.intervaltreetools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad.tools.intervaltreetools.compute_depth_of_intervals_in_interval import compute_depth_of_intervals_in_interval


def _make_voice_from_nonoverlapping_intervals(intervals, colorkey = None, bounds = None, pitch = None):

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return Voice([])
    assert all_intervals_are_nonoverlapping(tree)

    voice = Voice([])

#   if bounds is None:
#      depth_tree = compute_depth_of_intervals(tree)
#   else:
#      depth_tree = compute_depth_of_intervals_in_interval(tree, bounds)

    depth_tree = compute_depth_of_intervals_in_interval(tree, BoundedInterval(0, tree.high))

    if pitch is None:
        pitch = 0

    for i, depth_interval in enumerate(depth_tree):
        if depth_interval['depth'] == 0:
            if i == 0:
                rest = Rest(1)
                rest.duration_multiplier = depth_interval.magnitude
                voice.append(rest)
            else:
                note = Note(pitch, 1)
                note.duration_multiplier = depth_interval.magnitude
                note.override.note_head.transparent = True
                voice.append(note)
                GlissandoSpanner(voice[-2:])
#                note = Note(0, 1)
#                note.duration_multiplier = 0
#                note.override.note_head.transparent = True
#                voice.append(note)
#                GlissandoSpanner(voice[-2:])
#                rest = Rest(1)
#                rest.duration_multiplier = depth_interval.magnitude
#                voice.append(rest)

        elif depth_interval['depth'] == 1:
            note = Note(pitch, 1)
            note.duration_multiplier = depth_interval.magnitude
            if colorkey is not None:
                try:
                    original_interval = tree.find_intervals_starting_at_offset(depth_interval.low)[0]
                    color = SchemeColor(original_interval[colorkey])
                    note.override.note_head.color = color
                    note.override.glissando.color = color
                except KeyError:
                    pass
            voice.append(note)
            if i != 0 and 0 < depth_tree[i - 1]['depth']:
                GlissandoSpanner(voice[-2:])
            if depth_interval == depth_tree[-1]:
                note = Note(pitch, 1)
                note.override.note_head.transparent = True
                voice.append(note)
                GlissandoSpanner(voice[-2:])

        else:
            raise Exception('Intervals were not non-overlapping!')

    voice.engraver_removals.add('Forbid_line_break_engraver')

    return voice
