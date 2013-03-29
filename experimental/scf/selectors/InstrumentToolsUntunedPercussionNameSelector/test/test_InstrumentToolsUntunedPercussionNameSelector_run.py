import scf


def test_InstrumentToolsUntunedPercussionNameSelector_run_01():

    selector = scf.selectors.InstrumentToolsUntunedPercussionNameSelector()
    assert selector.run(user_input='cax') == 'caxixi'
