# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreManager_manage_svn_01():
    r'''Ignore score backtracking.
    '''

    score_manager = scoremanagertools.core.ScoreManager()
    score_manager._run(pending_user_input='rep sco q')
    assert score_manager.session.io_transcript.signature == (6, (2, 4))
