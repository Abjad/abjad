# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_write_stub_initializer_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        '__init__.py',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert filecmp.cmp(path, backup_path)
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score inws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        contents = score_manager._transcript.contents
        assert 'Will write stub to' in contents
        assert 'Wrote stub to' in contents
    finally:
        assert os.path.isfile(backup_path)
        shutil.copyfile(backup_path, path)
        assert filecmp.cmp(path, backup_path)
        os.remove(backup_path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)