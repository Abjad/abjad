import scftools


def test_ArticulationHandlerClassNameSelector_run_01():

    selector = scftools.selectors.ArticulationHandlerClassNameSelector()

    assert selector.run(user_input='reiterated') == 'ReiteratedArticulationHandler'
