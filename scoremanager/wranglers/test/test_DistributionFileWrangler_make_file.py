# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_make_file_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'distribution',
        'test-file.txt',
        )

    assert not os.path.exists(path)
    try:
        input_ = 'red~example~score d new test-file.txt q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)