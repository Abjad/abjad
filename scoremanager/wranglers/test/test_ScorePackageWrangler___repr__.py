# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler___repr___01():

    spw = scoremanager.wranglers.ScorePackageWrangler()

    assert repr(spw) == 'ScorePackageWrangler()'
