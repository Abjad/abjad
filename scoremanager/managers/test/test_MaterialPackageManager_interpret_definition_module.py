# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_interpret_definition_module_01():
    r'''Interpretation makes sure definition module raises no exceptions.
    '''

    input_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    input_ = 'red~example~score m magic~numbers dmi q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    string = 'No exceptions raised; use (omo) to write output module.'
    assert string in contents
    assert 'Interpreted' in contents