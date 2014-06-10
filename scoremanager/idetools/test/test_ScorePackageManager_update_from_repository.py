# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
score_manager._session._is_repository_test = True


def test_ScorePackageManager_update_from_repository_01():

    input_ = 'red~example~score rup <return> q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository