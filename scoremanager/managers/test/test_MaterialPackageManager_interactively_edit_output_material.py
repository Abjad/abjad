# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_interactively_edit_output_material_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'materials red~markup omi q'
    score_manager._run(pending_user_input=string)
    transcript = score_manager.session.io_transcript

    string = 'Score manager - materials - red markup - edit'
    assert transcript.last_menu_lines[0] == string
