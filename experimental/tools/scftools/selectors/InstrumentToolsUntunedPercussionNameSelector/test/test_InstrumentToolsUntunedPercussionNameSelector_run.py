from experimental import *


def test_InstrumentToolsUntunedPercussionNameSelector_run_01():

    selector = scftools.selectors.InstrumentToolsUntunedPercussionNameSelector()
    assert selector.run(user_input='cax') == 'caxixi'
