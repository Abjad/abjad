# -*- coding: utf-8 -*-
import abjad


def configure_score(score):
    r'''Configures score.
    '''

    spacing_vector = abjad.make_spacing_vector(0, 0, 8, 0)
    abjad.override(score).vertical_axis_group.staff_staff_spacing = \
        spacing_vector
    abjad.override(score).staff_grouper.staff_staff_spacing = spacing_vector
    abjad.override(score).staff_symbol.thickness = 0.5
    abjad.setting(score).mark_formatter = abjad.Scheme('format-mark-box-numbers')
