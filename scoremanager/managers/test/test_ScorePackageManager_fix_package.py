# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_fix_package_01():
    r'''Works when no fixes are required.
    '''

    input_ = 'red~example~score fix q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'No fixes required.' in contents


def test_ScorePackageManager_fix_package_02():
    r'''Works when no fixes are required.
    '''

    score_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        )

    initializer_path = os.path.join(score_path, '__init__.py')
    initializer_backup = initializer_path + '.backup'
    metadata_path = os.path.join(score_path, '__metadata__.py')
    metadata_backup = metadata_path + '.backup'

    assert os.path.isfile(initializer_path)
    assert os.path.isfile(metadata_path)
    assert not os.path.isfile(initializer_backup)
    assert not os.path.isfile(metadata_backup)

    try:
        shutil.copyfile(initializer_path, initializer_backup)
        shutil.copyfile(metadata_path, metadata_backup)
        assert os.path.isfile(initializer_backup)
        assert os.path.isfile(metadata_backup)
        os.remove(initializer_path)
        os.remove(metadata_path)
        # calls fix_package() on ScorePackageManager start
        input_ = 'red~example~score q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(initializer_path)
        assert os.path.isfile(metadata_path)
    finally:
        shutil.copyfile(initializer_backup, initializer_path)
        shutil.copyfile(metadata_backup, metadata_path)
        os.remove(initializer_backup)
        os.remove(metadata_backup)

    assert os.path.isfile(initializer_path)
    assert os.path.isfile(metadata_path)
    assert not os.path.exists(initializer_backup)
    assert not os.path.exists(metadata_backup)