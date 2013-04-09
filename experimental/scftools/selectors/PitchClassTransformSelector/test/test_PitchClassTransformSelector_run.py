import scftools


def test_PitchClassTransformSelector_run_01():

    selector = scftools.selectors.PitchClassTransformSelector()
    assert selector.run(user_input='q') is None
    assert selector.run(user_input='b') is None


def test_PitchClassTransformSelector_run_02():

    selector = scftools.selectors.PitchClassTransformSelector()
    assert selector.run(user_input='tra') == 'transpose'
    assert selector.run(user_input='inv') == 'invert'
    assert selector.run(user_input='mul') == 'multiply'
