from experimental import *


def test_ArticulationHandlerClassNameSelector_run_01():

    selector = scoremanagementtools.selectors.ArticulationHandlerClassNameSelector()

    assert selector.run(user_input='reiterated') == 'ReiteratedArticulationHandler'
