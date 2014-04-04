# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_manage_maker_library_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'k q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - maker module library',
        ]

    assert score_manager._transcript.titles == titles