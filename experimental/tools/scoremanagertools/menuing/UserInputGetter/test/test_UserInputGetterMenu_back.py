from experimental import *


def test_UserInputGetter_back_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='red~example~score setup performers move b q')
    assert score_manager._session.transcript.signature == (11, (6, 9))
