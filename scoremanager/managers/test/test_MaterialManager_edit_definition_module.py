# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_edit_definition_module_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'lmm example~numbers dme q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file
