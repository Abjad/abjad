# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_edit_output_material_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'lmm example~markup~inventory me q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    string = 'Score manager - material library -'
    string += ' example markup inventory - edit'
    assert transcript.last_title == string
