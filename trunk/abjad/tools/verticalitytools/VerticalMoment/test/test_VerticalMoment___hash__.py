from abjad import *
from abjad.tools import verticalitytools


def test_VerticalMoment___hash___01():
    '''Vertical moments behave well when included in a set.'''

    t = Staff("c'8 d'8 e'8 f'8")
    vms = []
    vms.extend(list(verticalitytools.iterate_vertical_moments_forward_in_expr(t)))
    vms.extend(list(verticalitytools.iterate_vertical_moments_forward_in_expr(t)))

    assert len(vms) == 8
    assert len(set(vms)) == 4
