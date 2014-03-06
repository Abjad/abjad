# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_edit_output_material_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'lmm example~markup~inventory omi q'
    score_manager._run(pending_user_input=string, is_test=True)
    transcript = score_manager._transcript

    string = 'Score manager - material library - example markup inventory - edit'
    assert transcript.last_title == string
