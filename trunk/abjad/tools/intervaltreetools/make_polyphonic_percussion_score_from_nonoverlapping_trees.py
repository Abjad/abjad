from abjad import Fraction
from abjad import Score
from abjad import Staff
from abjad.tools.contexttools import ClefMark
from abjad.tools.lilypondfiletools import make_basic_lilypond_file
from abjad.tools.pitchtools import make_n_middle_c_centered_pitches
from abjad.tools.schemetools import SchemeMoment
from abjad.tools.schemetools import SchemePair
from abjad.tools.schemetools import SchemeVector
from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools._make_voice_from_nonoverlapping_intervals import _make_voice_from_nonoverlapping_intervals
from collections import Iterable


def make_polyphonic_percussion_score_from_nonoverlapping_trees(trees, colorkey = None):
    '''Make a polyphonic percussion score from a collections of non-overlapping trees.'''

    assert isinstance(trees, Iterable) and len(trees) and \
        all([isinstance(tree, IntervalTree) for tree in trees])

    pitches = make_n_middle_c_centered_pitches(len(trees))
    bounds = BoundedInterval(min([x.low for x in trees]), max([x.high for x in trees]))
    voices = []
    for zipped in zip(trees, pitches):
        tree = zipped[0]
        pitch = zipped[1]
        voice = _make_voice_from_nonoverlapping_intervals(tree, \
            colorkey = colorkey, bounds = bounds, pitch = pitch)
        voices.append(voice)

    staff = Staff(voices)
    staff.is_parallel = True
    staff.override.staff_symbol.line_count = len(voices)
    ClefMark('percussion')(staff)

    score = Score([staff])
    score.override.glissando.thickness = 5
    score.override.note_head.style = 'harmonic'
    score.override.rest.transparent = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.spacing_spanner.uniform_stretching = True
    score.override.glissando.breakable = True
    score.set.proportional_notation_duration = SchemeMoment(Fraction(1, 32))
    padding = 0.5
    bound_details = SchemeVector( \
        SchemeVector('right', SchemePair('attach-dir', 0), SchemePair('padding', padding)),
        SchemeVector('left', SchemePair('attach-dir', 0), SchemePair('padding', padding)))
    score.override.glissando.bound_details = bound_details

    lily = make_basic_lilypond_file(score)
    lily.default_paper_size = ('11x17', 'landscape')
    lily.paper_block.ragged_right = True

    return lily
