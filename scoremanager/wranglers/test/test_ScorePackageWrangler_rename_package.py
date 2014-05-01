# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_ScorePackageWrangler_rename_package_01():
    r'''Creates score package. Renames score package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score',
        )
    new_path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'new_test_score',
        )

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        input_ = 'new test~score q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        input_ = 'ssl ren Untitled~(test_score) new_test_score y q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)