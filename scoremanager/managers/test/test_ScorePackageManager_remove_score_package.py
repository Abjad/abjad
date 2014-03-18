# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_ScorePackageManager_remove_score_package_01():
    r'''Creates score package. Removes score package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score',
        )
    input_ = 'new test~score q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        input_ = 'ssl Untitled~(test_score) rm clobber q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
