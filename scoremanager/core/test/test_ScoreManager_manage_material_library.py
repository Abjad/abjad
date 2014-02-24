# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_manage_material_library_01():
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q')

    string = 'Score manager - material library'
    assert score_manager._transcript.last_menu_title == string
