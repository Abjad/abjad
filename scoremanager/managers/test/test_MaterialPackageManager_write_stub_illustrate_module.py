# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_write_stub_illustrate_module_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert filecmp.cmp(path, backup_path)
        input_ = 'red~example~score m magic~numbers imws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, backup_path)
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