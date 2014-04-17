# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_pytest_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score pyt default q'
    score_manager._run(pending_user_input=input_)

    string = '3 testable assets found ...'
    assert score_manager._transcript.titles[-3] == string