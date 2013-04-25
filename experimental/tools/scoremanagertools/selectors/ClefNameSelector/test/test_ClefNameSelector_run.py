from experimental import *


def test_ClefNameSelector_run_01():

    selector = scoremanagertools.selectors.ClefNameSelector()

    assert selector.run(user_input='tre') == 'treble'
