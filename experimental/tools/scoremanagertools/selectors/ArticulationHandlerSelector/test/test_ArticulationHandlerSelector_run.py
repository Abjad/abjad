from experimental import *


def test_ArticulationHandlerSelector_run_01():

    selector = scoremanagertools.selectors.ArticulationHandlerSelector()

    assert selector._run(user_input='built_in_materials.red_mar') == 'built_in_materials.red_marcati'
