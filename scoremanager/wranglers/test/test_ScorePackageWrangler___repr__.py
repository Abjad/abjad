# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageWrangler___repr___01():

    spw = scoremanager.wranglers.ScorePackageWrangler()

    assert repr(spw) == 'ScorePackageWrangler()'
