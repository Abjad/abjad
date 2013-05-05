# -*- encoding: utf-8 -*-
from experimental import *


# TODO: remove test from experimental branch or change to something that runs on all systems
def test_ScorePackageProxy_edit_title_interactively_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager.run(user_input='betorung setup title Foo q')
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Betörung (2012) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Foo (2012) - setup'
    finally:
        score_manager.run(user_input='foo setup title Betörung q')
        assert score_manager.session.transcript.signature == (9,)
        assert score_manager.session.transcript[-5][1][0] == 'Foo (2012) - setup'
        assert score_manager.session.transcript[-2][1][0] == 'Betörung (2012) - setup'
