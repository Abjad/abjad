# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_interpret_back_cover_01():
    r'''Works when back cover already exists.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'back-cover.tex',
        )
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'back-cover.pdf',
        )
    backup_path = path + '.backup'
    assert os.path.isfile(source_path)
    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert filecmp.cmp(path, backup_path)
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u bci q'
        score_manager._run(pending_user_input=input_)
        assert os.path.isfile(path)
        #assert pdfcmp(path, backup_path)
    finally:
        assert os.path.exists(backup_path)
        if os.path.exists(path):
            os.remove(path)
        shutil.copyfile(backup_path, path)
        os.remove(backup_path)

    assert os.path.isfile(source_path)
    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)