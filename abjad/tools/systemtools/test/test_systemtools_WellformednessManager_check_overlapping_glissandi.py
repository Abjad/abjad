# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_WellformednessManager_check_overlapping_glissandi_01():

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.attach(abjad.Glissando(), staff[:2])
    abjad.attach(abjad.Glissando(), staff[1:3])

    assert abjad.inspect(staff).is_well_formed()


def test_systemtools_WellformednessManager_check_overlapping_glissandi_02():

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.attach(abjad.Glissando(), staff[:2])
    abjad.attach(abjad.Glissando(), staff[:3])

    assert not abjad.inspect(staff).is_well_formed()
