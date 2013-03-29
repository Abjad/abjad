import scf


def test_ClefNameSelector_run_01():

    selector = scf.selectors.ClefNameSelector()

    assert selector.run(user_input='tre') == 'treble'
