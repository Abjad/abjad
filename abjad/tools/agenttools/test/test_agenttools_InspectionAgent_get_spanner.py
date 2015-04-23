# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_spanner_01():

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container.select_leaves()[:-1])
    slur = Slur()
    attach(slur, container.select_leaves()[:-1])
    trill = spannertools.TrillSpanner()
    attach(trill, container)

    assert systemtools.TestManager.compare(
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

    assert inspect_(container).get_spanner() == trill

    string = 'inspect_(container[0]).get_spanner()'
    assert pytest.raises(Exception, string)

    string = 'inspect_(container[-1]).get_spanner()'
    assert pytest.raises(Exception, string)


def test_agenttools_InspectionAgent_get_spanner_02():

    staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 } g'2")
    slur = Slur()
    attach(slur, staff[:])
    for leaf in staff.select_leaves():
        assert slur == inspect_(leaf).get_spanner(Slur, in_parentage=True)