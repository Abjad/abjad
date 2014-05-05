# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_open_illustration_ly_01():

    input_ = 'red~example~score m magic~numbers lyo q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file