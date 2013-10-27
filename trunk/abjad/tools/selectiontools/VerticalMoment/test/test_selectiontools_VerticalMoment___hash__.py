# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment___hash___01():
    r'''Vertical moments behave well when included in a set.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    vms = []
    vms.extend(list(iterationtools.iterate_vertical_moments_in_expr(staff)))
    vms.extend(list(iterationtools.iterate_vertical_moments_in_expr(staff)))

    assert len(vms) == 8
    assert len(set(vms)) == 4
