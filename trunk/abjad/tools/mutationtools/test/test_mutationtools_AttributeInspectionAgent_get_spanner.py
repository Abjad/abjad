# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_mutationtools_AttributeInspectionAgent_get_spanner_01():

    container = Container("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    attach(beam, container.select_leaves()[:-1])
    slur = spannertools.SlurSpanner()
    attach(slur, container.select_leaves()[:-1])
    trill = spannertools.TrillSpanner()
    trill.attach(container)

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

    assert inspect(container).get_spanner() == trill

    string = 'inspect(container[0]).get_spanner()'
    assert py.test.raises(ExtraSpannerError, string)

    string = 'inspect(container[-1]).get_spanner()'
    assert py.test.raises(MissingSpannerError, string)
