# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_edit_metadata_module_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm example~numbers mdmo q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file