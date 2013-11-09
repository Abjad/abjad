# -*- encoding: utf-8 -*-
from abjad import *


def configure_score(score):
    contextualize(score).proportional_notation_duration = schemetools.SchemeMoment(1, 56)
    contextualize(score).tuplet_full_length = True
    override(score).bar_line.stencil = False
    override(score).bar_number.transparent = True
    override(score).spacing_spanner.uniform_stretching = True
    override(score).spacing_spanner.strict_note_spacing = True
    override(score).time_signature.stencil = False
    override(score).tuplet_bracket.padding = 2
    override(score).tuplet_bracket.staff_padding = 4
    override(score).tuplet_number.text = \
        schemetools.Scheme('tuplet-number::calc-fraction-text')
