# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_rename_package_01():
    r'''Creates score package. Renames score package.
    '''

    path_100 = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'example_score_100',
        )
    path_101 = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'example_score_101',
        )

    assert not os.path.exists(path_100)
    assert not os.path.exists(path_101)
    try:
        input_ = 'new example~score~100 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path_100)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_100, session=score_manager._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        input_ = 'ren Example~Score~100 example_score_101 y q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path_100)
        assert os.path.exists(path_101)
    finally:
        if os.path.exists(path_100):
            shutil.rmtree(path_100)
        if os.path.exists(path_101):
            shutil.rmtree(path_101)
    assert not os.path.exists(path_100)
    assert not os.path.exists(path_101)