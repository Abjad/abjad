from experimental import *


def test_ParameterEditorClassNameSelector_run_01():

    selector = scoremanagementtools.selectors.ParameterEditorClassNameSelector()

    assert selector.run(user_input='trop') == 'TropingSpecifierEditor'
