# -*- encoding: utf-8 -*-
from abjad import *


def configure_score(score):

    spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
    override(score).vertical_axis_group.staff_staff_spacing = spacing_vector
    override(score).staff_grouper.staff_staff_spacing = spacing_vector
    override(score).staff_symbol.thickness = 0.5
    score.set.mark_formatter = schemetools.Scheme('format-mark-box-numbers')
