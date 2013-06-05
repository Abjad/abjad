# -*- encoding: utf-8 -*-
from experimental import *
import py
py.test.skip('unskip me after making decision about cache.')


def test_ScorePackageProxy_interactively_edit_title_01():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager._run(user_input='green~example~score setup title Foo q')
        assert score_manager._session.transcript.signature == (9,)
        assert score_manager._session.transcript[-5][1][0] == 'Green Example Score (2013) - setup'
        assert score_manager._session.transcript[-2][1][0] == 'Foo (2013) - setup'
    finally:
        score_manager._run(user_input='foo setup title Green~Example~Score q')
        assert score_manager._session.transcript.signature == (9,)
        assert score_manager._session.transcript[-5][1][0] == 'Foo (2013) - setup'
        assert score_manager._session.transcript[-2][1][0] == 'Green Example Score (2013) - setup'
