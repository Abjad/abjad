from experimental import *


def test_ClefNameSelector_run_01():

    selector = scoremanagementtools.selectors.ClefNameSelector()

    assert selector.run(user_input='tre') == 'treble'
