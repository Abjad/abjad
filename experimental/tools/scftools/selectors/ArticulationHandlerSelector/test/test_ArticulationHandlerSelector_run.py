from experimental import *


def test_ArticulationHandlerSelector_run_01():

    selector = scftools.selectors.ArticulationHandlerSelector()

    assert selector.run(user_input='materials.red_mar') == 'materials.red_marcati'
