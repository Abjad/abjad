# -*- encoding: utf-8 -*-
from abjad import *

def test_spannertools_get_spanners_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.select_leaves())
    first_slur = spannertools.SlurSpanner(staff.select_leaves()[:2])
    second_slur = spannertools.SlurSpanner(staff.select_leaves()[2:])
    crescendo = spannertools.CrescendoSpanner(staff.select_leaves())

    r'''
    \new Staff {
        c'8 [ \< (
        d'8 )
        e'8 (
        f'8 ] \! )
    }
    '''

    leaf = staff[0]

    spanners = spannertools.get_spanners_attached_to_component(leaf)
    assert spanners == set([beam, first_slur, crescendo])

    spanner_classes = (spannertools.BeamSpanner, )
    spanners = spannertools.get_spanners_attached_to_component(
        leaf, spanner_classes=spanner_classes)
    assert spanners == set([beam])

    spanner_classes = (spannertools.BeamSpanner, spannertools.SlurSpanner)
    spanners = spannertools.get_spanners_attached_to_component(
        leaf, spanner_classes)
    assert spanners == set([beam, first_slur])

    spanner_classes = (spannertools.TieSpanner, )
    spanners = spannertools.get_spanners_attached_to_component(
        leaf, spanner_classes=spanner_classes)
    assert spanners == set([])
