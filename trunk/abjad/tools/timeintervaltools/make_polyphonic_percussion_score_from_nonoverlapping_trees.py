import collections
import fractions
from abjad.tools import contexttools
from abjad.tools import lilypondfiletools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import stafftools


def make_polyphonic_percussion_score_from_nonoverlapping_trees(trees, colorkey=None):
    '''Make a polyphonic percussion score from a collections of non-overlapping trees.

    Return LilyPondFile.
    '''

    from abjad.tools import timeintervaltools

    if isinstance(trees, timeintervaltools.TimeIntervalTreeDictionary):
        trees = trees.values()
    else:
        assert isinstance(trees, collections.Iterable) and len(trees) and \
            all([isinstance(tree, timeintervaltools.TimeIntervalTree) for tree in trees])
    

    pitches = pitchtools.make_n_middle_c_centered_pitches(len(trees))
    voices = []
    for zipped in zip(trees, pitches):
        tree = zipped[0]
        pitch = zipped[1]
        voice = timeintervaltools.make_voice_from_nonoverlapping_intervals(tree,
            colorkey = colorkey, pitch = pitch)
        voices.append(voice)

    staff = stafftools.Staff(voices)
    staff.is_parallel = True
    staff.override.staff_symbol.line_count = len(voices)
    contexttools.ClefMark('percussion')(staff)

    score = scoretools.Score([staff])
    score.override.glissando.thickness = 5
    score.override.note_head.style = 'harmonic'
    score.override.rest.transparent = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.spacing_spanner.uniform_stretching = True
    score.override.glissando.breakable = True
    score.set.proportional_notation_duration = schemetools.SchemeMoment(fractions.Fraction(1, 32))
    padding = 0.5
    bound_details = schemetools.Scheme(
        ('right',
            schemetools.SchemePair('attach-dir', 0),
            schemetools.SchemePair('padding', padding)),
        ('left',
            schemetools.SchemePair('attach-dir', 0),
            schemetools.SchemePair('padding', padding)),
        quoting="'")
    score.override.glissando.bound_details = bound_details

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.default_paper_size = ('11x17', 'landscape')
    lily.paper_block.ragged_right = True

    return lily
