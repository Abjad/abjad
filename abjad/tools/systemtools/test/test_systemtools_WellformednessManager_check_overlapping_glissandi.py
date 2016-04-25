# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_WellformednessManager_check_overlapping_glissandi_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    attach(Glissando(), staff[:2])
    attach(Glissando(), staff[1:3])

    assert inspect_(staff).is_well_formed()


def test_systemtools_WellformednessManager_check_overlapping_glissandi_02():

    staff = Staff("c'4 d'4 e'4 f'4")
    attach(Glissando(), staff[:2])
    attach(Glissando(), staff[:3])

    assert not inspect_(staff).is_well_formed()
