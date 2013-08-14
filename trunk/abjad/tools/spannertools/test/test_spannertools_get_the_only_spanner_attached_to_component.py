# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_get_the_only_spanner_attached_to_component_01():

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

    assert spannertools.get_the_only_spanner_attached_to_component(container) == trill

    assert py.test.raises(ExtraSpannerError,
        'spannertools.get_the_only_spanner_attached_to_component(container[0])')

    assert py.test.raises(MissingSpannerError,
        'spannertools.get_the_only_spanner_attached_to_component(container[-1])')
