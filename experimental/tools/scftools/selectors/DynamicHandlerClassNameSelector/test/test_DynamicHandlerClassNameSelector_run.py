from experimental import *


def test_DynamicHandlerClassNameSelector_run_01():

    selector = scftools.selectors.DynamicHandlerClassNameSelector()

    assert selector.run(user_input='terraced') == 'TerracedDynamicsHandler'
