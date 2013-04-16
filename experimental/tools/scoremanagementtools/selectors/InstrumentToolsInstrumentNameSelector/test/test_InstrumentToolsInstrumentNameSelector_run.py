from experimental import *


def test_InstrumentToolsInstrumentNameSelector_run_01():

    selector = scoremanagementtools.selectors.InstrumentToolsInstrumentNameSelector()
    assert selector.run(user_input='marimba') == 'marimba'
