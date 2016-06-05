# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_format_01():
    r'''Base Spanner class makes no format-time contributions.
    However, base spanner causes no explosions at format-time, either.
    '''

    class MockSpanner(spannertools.Spanner):

        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)

    staff = Staff("c'8 d'8 e'8 f'8")
    spanner = MockSpanner()
    attach(spanner, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
