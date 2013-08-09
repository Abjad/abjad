# -*- encoding: utf-8 -*-
from abjad import *


def test_Spanner_format_01():
    r'''Base Spanner class makes no format-time contributions.
    However, base spanner causes no explosions at format-time, either.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    staff = Staff("c'8 d'8 e'8 f'8")
    spanner = MockSpanner(staff[:])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
