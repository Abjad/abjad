# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentToolsInstrumentNameSelector_run_01():

    selector = scoremanagertools.selectors.InstrumentToolsInstrumentNameSelector()
    assert selector._run(pending_user_input='marimba') == 'marimba'
