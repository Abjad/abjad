# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_generate_score_source_01():
    r'''Works when score source already exists.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'score.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert filecmp.cmp(path, backup_path)
        assert os.path.exists(backup_path)
        input_ = 'red~example~score u sg y q'
        score_manager._run(pending_user_input=input_)
        assert os.path.isfile(path)
        assert filecmp.cmp(path, backup_path)
    finally:
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, path)
        if os.path.exists(backup_path):
            os.remove(backup_path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)