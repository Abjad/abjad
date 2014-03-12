# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_edit_material_definition_module_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'lmm example~numbers mde q'
    score_manager._run(pending_user_input=input_, is_test=True)

    assert score_manager._session.attempted_to_open_file
