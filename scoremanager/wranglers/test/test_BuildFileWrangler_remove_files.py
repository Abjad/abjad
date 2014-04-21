# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_remove_files_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'foo-file.txt',
        )

    assert not os.path.exists(path)
    try:
        with file(path, 'w') as file_pointer:
            file_pointer.write('This is a test file.')
        assert os.path.exists(path)
        input_ = 'red~example~score u rm foo-file.txt remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)