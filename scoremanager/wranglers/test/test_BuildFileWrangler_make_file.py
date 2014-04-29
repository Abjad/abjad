# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_BuildFileWrangler_make_file_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'test-file.txt',
        )

    assert not os.path.exists(path)
    try:
        input_ = 'red~example~score u new test-file.txt q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)