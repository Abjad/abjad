# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator__init_by_reference_01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)
    u = tonalanalysistools.SuspensionIndicator(t)

    assert t is not u
    assert t == u
