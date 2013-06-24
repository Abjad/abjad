from experimental import *


def test_InstrumentToolsUntunedPercussionNameSelector_run_01():

    selector = scoremanagertools.selectors.InstrumentToolsUntunedPercussionNameSelector()
    assert selector._run(pending_user_input='cax') == 'caxixi'
