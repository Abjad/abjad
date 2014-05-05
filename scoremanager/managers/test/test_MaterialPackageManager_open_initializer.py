# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_open_initializer_01():

    input_ = 'red~example~score m magic~numbers ino q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file