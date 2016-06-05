# -*- coding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def configure_score(score):
    r'''Configures score.
    '''

    spacing_vector = schemetools.make_spacing_vector(0, 0, 8, 0)
    override(score).vertical_axis_group.staff_staff_spacing = spacing_vector
    override(score).staff_grouper.staff_staff_spacing = spacing_vector
    override(score).staff_symbol.thickness = 0.5
    set_(score).mark_formatter = schemetools.Scheme('format-mark-box-numbers')