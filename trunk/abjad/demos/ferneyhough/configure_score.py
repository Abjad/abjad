from abjad import *


def configure_score(score):
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 56)
    score.set.tuplet_full_length = True
    score.override.bar_line.stencil = False
    score.override.bar_number.transparent = True
    score.override.spacing_spanner.uniform_stretching = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.time_signature.stencil = False
    score.override.tuplet_bracket.padding = 2
    score.override.tuplet_bracket.staff_padding = 4
    score.override.tuplet_number.text = schemetools.Scheme('tuplet-number::calc-fraction-text')
    pass
