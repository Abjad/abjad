import scf


def test_DynamicHandlerClassNameSelector_run_01():

    selector = scf.selectors.DynamicHandlerClassNameSelector()

    assert selector.run(user_input='terraced') == 'TerracedDynamicsHandler'
