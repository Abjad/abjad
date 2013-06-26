from experimental import *


def test_UserInputGetter_exec_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers move exec 2**30 q')
    assert score_manager.session.io_transcript.signature == (12,)
