# -*- encoding: utf-8 -*-
from experimental import *


def test_PitchClassTransformSelector_run_01():

    selector = scoremanagertools.selectors.PitchClassTransformSelector()
    assert selector._run(pending_user_input='q') is None
    assert selector._run(pending_user_input='b') is None


def test_PitchClassTransformSelector_run_02():

    selector = scoremanagertools.selectors.PitchClassTransformSelector()
    assert selector._run(pending_user_input='tra') == 'transpose'
    assert selector._run(pending_user_input='inv') == 'invert'
    assert selector._run(pending_user_input='mul') == 'multiply'
