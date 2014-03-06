# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PackageManager_view_initializer_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'lmm example~numbers inv q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores', 
        'Score manager - material library',
        'Score manager - material library - example numbers', 
        'Score manager - material library - example numbers',
        ]
    assert score_manager._transcript.titles == titles
    assert score_manager._session.attempted_to_open_file
