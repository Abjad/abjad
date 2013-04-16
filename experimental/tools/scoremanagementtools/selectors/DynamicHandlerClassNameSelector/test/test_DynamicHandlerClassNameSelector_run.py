from experimental import *


def test_DynamicHandlerClassNameSelector_run_01():

    selector = scoremanagementtools.selectors.DynamicHandlerClassNameSelector()

    assert selector.run(user_input='terraced') == 'TerracedDynamicsHandler'
