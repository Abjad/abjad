from abjad import *


def configure_score(score):

    spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
    score.override.vertical_axis_group.staff_staff_spacing = spacing_vector
    score.override.staff_grouper.staff_staff_spacing = spacing_vector
    score.override.staff_symbol.thickness = 0.5
    score.set.mark_formatter = schemetools.Scheme('format-mark-box-numbers')
