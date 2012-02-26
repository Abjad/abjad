from abjad import Score
from abjad import Staff
from abjad.tools.contexttools import ClefMark
from abjad.tools.schemetools import Scheme
from abjad.tools.schemetools import SchemePair
from abjad.tools.intervaltreetools._make_voice_from_nonoverlapping_intervals import _make_voice_from_nonoverlapping_intervals


def make_monophonic_percussion_score_from_nonoverlapping_intervals(intervals, colorkey = None):
    '''Create a monophonic percussion score from nonoverlapping interval collection `intervals`.'''

    voice = _make_voice_from_nonoverlapping_intervals(intervals, colorkey)

    staff = Staff(voice[:])
    staff.override.staff_symbol.line_count = 1
    ClefMark('percussion')(staff)

    score = Score([staff])
    score.override.glissando.thickness = 5
    score.override.note_head.style = 'harmonic'
    score.override.rest.transparent = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.glissando.breakable = True
    padding = 0.5
    bound_details = Scheme(('right', SchemePair('attach-dir', 0), SchemePair('padding', padding)),
        ('left', SchemePair('attach-dir', 0), SchemePair('padding', padding)), quoting="'")
    score.override.glissando.bound_details = bound_details

    return score
