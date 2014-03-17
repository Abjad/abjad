# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_ScorePackageManager_rename_score_package_01():
    r'''Creates score package. Renames score package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score',
        )
    new_path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'new_test_score',
        )
    input_ = 'new test~score q'

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        input_ = 'ssl Untitled~(test_score) ren new~test~score y default q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
