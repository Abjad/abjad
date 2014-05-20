# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_interpret_definition_py_01():
    r'''Interpretation makes sure definition py raises no exceptions.
    '''

    input_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    input_ = 'red~example~score m magic~numbers di q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Interpreted' in contents