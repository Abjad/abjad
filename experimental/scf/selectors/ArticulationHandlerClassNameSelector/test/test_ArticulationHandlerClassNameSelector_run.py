import scf


def test_ArticulationHandlerClassNameSelector_run_01():

    selector = scf.selectors.ArticulationHandlerClassNameSelector()

    assert selector.run(user_input='reiterated') == 'ReiteratedArticulationHandler'
