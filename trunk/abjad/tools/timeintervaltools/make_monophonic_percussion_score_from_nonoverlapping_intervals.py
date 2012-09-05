from abjad.tools import contexttools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import stafftools


def make_monophonic_percussion_score_from_nonoverlapping_intervals(intervals, colorkey=None):
    '''Create a monophonic percussion score from nonoverlapping interval collection `intervals`.

    Return Score.
    '''
    from abjad.tools import timeintervaltools

    voice = timeintervaltools.make_voice_from_nonoverlapping_intervals(intervals, colorkey)

    staff = stafftools.Staff(voice[:])
    staff.override.staff_symbol.line_count = 1
    contexttools.ClefMark('percussion')(staff)

    score = scoretools.Score([staff])
    score.override.glissando.thickness = 5
    score.override.note_head.style = 'harmonic'
    score.override.rest.transparent = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.glissando.breakable = True

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

    return score
