import scf


def test_ArticulationHandlerSelector_run_01():

    selector = scf.selectors.ArticulationHandlerSelector()

    assert selector.run(user_input='materials.red_mar') == 'materials.red_marcati'
