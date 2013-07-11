from abjad import *


def test_BeamSpanner_is_beamable_component_01():
    '''Eighth notes are beamable.
    Quarter notes are not beamable.
    '''

    assert beamtools.BeamSpanner.is_beamable_component(Note(0, (1, 8)))
    assert not beamtools.BeamSpanner.is_beamable_component(Note("c'4"))


def test_BeamSpanner_is_beamable_component_02():
    '''Containers are not beamable.
    '''

    assert not beamtools.BeamSpanner.is_beamable_component(Staff([]))
