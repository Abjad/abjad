# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_DirectoryManager_display_present_working_directory_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'lmm example~numbers pwd q'
    score_manager._run(pending_user_input=input_, is_test=True)
    path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'example_numbers',
        )
    assert score_manager._transcript.last_title == path
