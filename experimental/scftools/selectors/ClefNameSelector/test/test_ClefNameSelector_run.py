import scftools


def test_ClefNameSelector_run_01():

    selector = scftools.selectors.ClefNameSelector()

    assert selector.run(user_input='tre') == 'treble'
