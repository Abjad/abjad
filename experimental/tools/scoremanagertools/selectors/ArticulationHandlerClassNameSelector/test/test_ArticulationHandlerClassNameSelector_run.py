from experimental import *


def test_ArticulationHandlerClassNameSelector_run_01():

    selector = scoremanagertools.selectors.ArticulationHandlerClassNameSelector()

    assert selector._run(user_input='reiterated') == 'ReiteratedArticulationHandler'
