# -*- encoding: utf-8 -*-
from experimental import *


def test_UserInputGetter_back_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup performers move b q')
    assert score_manager.session.io_transcript.signature == (11, (6, 9))
