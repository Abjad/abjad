from experimental import *


def test_InstrumentToolsInstrumentNameSelector_run_01():

    selector = scoremanagertools.selectors.InstrumentToolsInstrumentNameSelector()
    assert selector._run(user_input='marimba') == 'marimba'
