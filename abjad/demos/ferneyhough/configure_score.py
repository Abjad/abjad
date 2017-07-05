# -*- coding: utf-8 -*-
import abjad


def configure_score(score):
    r'''Configures `score`.
    '''

    moment = abjad.SchemeMoment(1, 56)
    abjad.set_(score).proportional_notation_duration = moment
    abjad.set_(score).tuplet_full_length = True
    abjad.override(score).bar_line.stencil = False
    abjad.override(score).bar_number.transparent = True
    abjad.override(score).spacing_spanner.uniform_stretching = True
    abjad.override(score).spacing_spanner.strict_note_spacing = True
    abjad.override(score).time_signature.stencil = False
    abjad.override(score).tuplet_bracket.padding = 2
    abjad.override(score).tuplet_bracket.staff_padding = 4
    scheme = abjad.Scheme('tuplet-number::calc-fraction-text')
    abjad.override(score).tuplet_number.text = scheme
