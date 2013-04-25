from experimental import *


def test_ParameterEditorClassNameSelector_run_01():

    selector = scoremanagertools.selectors.ParameterEditorClassNameSelector()

    assert selector.run(user_input='trop') == 'TropingSpecifierEditor'
