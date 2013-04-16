from experimental import *


def test_ParameterSpecifierClassNameSelector_run_01():

    selector = scoremanagementtools.selectors.ParameterSpecifierClassNameSelector()
    assert selector.run(user_input='troping') == 'TropingSpecifier'
