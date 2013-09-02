# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Parentage__get_spanner_01():
    r'''Without spanner classes filter.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(container.select_leaves()[:-1])
    slur = spannertools.SlurSpanner(container.select_leaves()[:-1])
    trill = spannertools.TrillSpanner(container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8 ] )
            f'8 \stopTrillSpan
        }
        '''
        )

    assert container._get_parentage()._get_spanner() == trill

    string = 'container[0]._get_parentage()._get_spanner()'
    assert py.test.raises(ExtraSpannerError, string)

    assert container[-1]._get_parentage()._get_spanner() == trill
