import scf


def test_ParameterSpecifierClassNameSelector_run_01():

    selector = scf.selectors.ParameterSpecifierClassNameSelector()
    assert selector.run(user_input='troping') == 'TropingSpecifier'
