# -*- encoding: utf-8 -*-
from abjad import *


def test_BeamSpanner_is_beamable_component_01():
    r'''Eighth notes are beamable.
    Quarter notes are not beamable.
    '''

    assert spannertools.BeamSpanner.is_beamable_component(Note(0, (1, 8)))
    assert not spannertools.BeamSpanner.is_beamable_component(Note("c'4"))


def test_BeamSpanner_is_beamable_component_02():
    r'''Containers are not beamable.
    '''

    assert not spannertools.BeamSpanner.is_beamable_component(Staff([]))
