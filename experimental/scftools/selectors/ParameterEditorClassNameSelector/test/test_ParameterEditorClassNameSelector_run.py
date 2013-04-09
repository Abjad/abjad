import scftools


def test_ParameterEditorClassNameSelector_run_01():

    selector = scftools.selectors.ParameterEditorClassNameSelector()

    assert selector.run(user_input='trop') == 'TropingSpecifierEditor'
