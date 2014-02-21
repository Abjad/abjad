# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_interactively_edit_output_material_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'lmm red~markup omi q'
    score_manager._run(pending_user_input=string)
    transcript = score_manager._session.transcript

    string = 'Score manager - material library - red markup - edit'
    assert transcript.last_menu_title == string
