# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_interpret_definition_py_01():
    r'''Interpretation makes sure definition py raises no exceptions.
    '''

    input_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    input_ = 'red~example~score m magic~numbers dmi q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = 'No exceptions raised; use (omo) to write output py.'
    assert string in contents
    assert 'Interpreted' in contents