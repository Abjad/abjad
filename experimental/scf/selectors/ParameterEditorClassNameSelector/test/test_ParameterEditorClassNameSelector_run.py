import scf


def test_ParameterEditorClassNameSelector_run_01():

    selector = scf.selectors.ParameterEditorClassNameSelector()

    assert selector.run(user_input='trop') == 'TropingSpecifierEditor'
