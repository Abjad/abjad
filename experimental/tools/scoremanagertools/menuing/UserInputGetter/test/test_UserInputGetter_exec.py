from experimental import *


def test_UserInputGetter_exec_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers move exec 2**30 q')
    assert score_manager._session.transcript.signature == (12,)
