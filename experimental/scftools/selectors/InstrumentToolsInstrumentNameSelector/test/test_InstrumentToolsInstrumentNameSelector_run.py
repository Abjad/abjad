import scftools


def test_InstrumentToolsInstrumentNameSelector_run_01():

    selector = scftools.selectors.InstrumentToolsInstrumentNameSelector()
    assert selector.run(user_input='marimba') == 'marimba'
