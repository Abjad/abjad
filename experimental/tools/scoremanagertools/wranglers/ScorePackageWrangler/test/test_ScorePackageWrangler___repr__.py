from experimental import *


def test_ScorePackageWrangler___repr___01():

    spw = scoremanagertools.wranglers.ScorePackageWrangler()

    assert repr(spw) == 'ScorePackageWrangler()'
