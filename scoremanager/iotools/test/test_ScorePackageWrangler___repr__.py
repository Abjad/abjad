# -*- encoding: utf-8 -*-
import shutil
from abjad import *
import scoremanager


def test_ScorePackageWrangler___repr___01():

    session = scoremanager.iotools.Session(is_test=True)
    wrangler = scoremanager.iotools.ScorePackageWrangler(session=session)

    assert repr(wrangler) == 'ScorePackageWrangler()'