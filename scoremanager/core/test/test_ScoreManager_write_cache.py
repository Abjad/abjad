# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_write_cache_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._run(pending_user_input='cw default q', is_test=True)

    string = 'Cache written.'
    transcript = score_manager._transcript
    assert transcript[2].title.startswith(string)
