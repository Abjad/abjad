# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_ScoreManager_write_cache_01():
    pytest.skip('figure out good assert')
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='cw default q')
    string = 'Score manager - all scores'
    assert score_manager._session.io_transcript.last_menu_title == string
