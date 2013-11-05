# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override


def make_rhythmic_sketch_staff(music):
    r'''Make rhythmic staff with transparent time_signature and transparent bar
    lines.
    '''
    from abjad.tools import scoretools

    staff = scoretools.Staff(music)
    staff.context_name = 'RhythmicStaff'
    override(staff).time_signature.transparent = True
    override(staff).bar_line.transparent = True

    return staff
