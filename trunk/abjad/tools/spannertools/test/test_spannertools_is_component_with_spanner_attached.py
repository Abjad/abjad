# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_is_component_with_spanner_attached_01():
    r'''True when expr is a component with spanner attached.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.select_leaves())
    f(staff)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert spannertools.is_component_with_spanner_attached(staff[0])
    assert not spannertools.is_component_with_spanner_attached(staff)


def test_spannertools_is_component_with_spanner_attached_02():
    r'''True when expr is a component with spanner of class attached.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.select_leaves())
    f(staff)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert spannertools.is_component_with_spanner_attached(
        staff[0], spanner_classes=(spannertools.BeamSpanner,))
        
    assert not spannertools.is_component_with_spanner_attached(
        staff[0], spanner_classes=(spannertools.SlurSpanner,))
