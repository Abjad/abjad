from experimental import *


def test_DynamicHandlerClassNameSelector_run_01():

    selector = scoremanagertools.selectors.DynamicHandlerClassNameSelector()

    assert selector.run(user_input='terraced') == 'TerracedDynamicsHandler'
