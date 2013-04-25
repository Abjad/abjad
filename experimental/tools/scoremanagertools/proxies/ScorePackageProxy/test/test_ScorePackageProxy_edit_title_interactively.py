# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_title_interactively_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager.run(user_input='betorung setup title Foo q')
        assert score_manager.ts == (9,)
        assert score_manager.transcript[-5][0] == 'Betörung (2012) - setup'
        assert score_manager.transcript[-2][0] == 'Foo (2012) - setup'
    finally:
        score_manager.run(user_input='foo setup title Betörung q')
        assert score_manager.ts == (9,)
        assert score_manager.transcript[-5][0] == 'Foo (2012) - setup'
        assert score_manager.transcript[-2][0] == 'Betörung (2012) - setup'
