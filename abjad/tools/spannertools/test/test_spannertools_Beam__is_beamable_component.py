# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Beam__is_beamable_component_01():
    r'''Eighth notes are beamable.
    Quarter notes are not beamable.
    '''

    assert Beam._is_beamable_component(Note(0, (1, 8)))
    assert not Beam._is_beamable_component(Note("c'4"))


def test_spannertools_Beam__is_beamable_component_02():
    r'''Containers are not beamable.
    '''

    assert not Beam._is_beamable_component(Staff([]))
