# -*- coding: utf-8 -*-
import abjad


def configure_score(score):
    r'''Configures score.
    '''

    vector = abjad.SpacingVector(0, 0, 8, 0)
    abjad.override(score).vertical_axis_group.staff_staff_spacing = vector
    abjad.override(score).staff_grouper.staff_staff_spacing = vector
    abjad.override(score).staff_symbol.thickness = 0.5
    scheme = abjad.Scheme('format-mark-box-numbers')
    abjad.setting(score).mark_formatter = scheme
