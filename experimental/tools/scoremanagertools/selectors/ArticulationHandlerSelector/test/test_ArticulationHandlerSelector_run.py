from experimental import *


def test_ArticulationHandlerSelector_run_01():

    selector = scoremanagertools.selectors.ArticulationHandlerSelector()

    assert selector._run(user_input='experimental.tools.scoremanagertools.materialpackages.red_mar') == 'experimental.tools.scoremanagertools.materialpackages.red_marcati'
