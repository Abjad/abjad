# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Component__has_spanner_01():

    staff = Staff("c'8 [ d'8 e'8 f'8 ]")
    assert staff[0]._has_spanner(Beam)


def test_scoretools_Component__has_spanner_02():

    assert not Note("c'8")._has_spanner(Beam)
