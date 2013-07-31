# -*- encoding: utf-8 -*-
from experimental import *
import py
py.test.skip('unskip after where automatically toggles where-tracking.')


def test_UserInputGetter_where_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers move where q')
    assert score_manager.session.io_transcript.signature == (11,)
