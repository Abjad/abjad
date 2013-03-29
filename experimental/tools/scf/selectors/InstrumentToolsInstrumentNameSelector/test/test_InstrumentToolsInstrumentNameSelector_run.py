import scf


def test_InstrumentToolsInstrumentNameSelector_run_01():

    selector = scf.selectors.InstrumentToolsInstrumentNameSelector()
    assert selector.run(user_input='marimba') == 'marimba'
