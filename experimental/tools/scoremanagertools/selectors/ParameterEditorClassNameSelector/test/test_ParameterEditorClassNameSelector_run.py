from experimental import *


def test_ParameterEditorClassNameSelector_run_01():

    selector = scoremanagertools.selectors.ParameterEditorClassNameSelector()

    assert selector._run(pending_user_input='trop') == 'TropingSpecifierEditor'
