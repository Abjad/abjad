# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_remove_packages_01():
    r'''Removes one score package.
    '''

    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'example_score_100',
        )

    assert not os.path.exists(path)
    try:
        input_ = 'new example~score~100 q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=score_manager._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        input_ = 'rm Example~Score~100 remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_ScorePackageWrangler_remove_packages_02():
    r'''Removes range of score packages.
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
    try:
        input_ = 'new example~score~100 new example~score~101 q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path_100)
        assert os.path.exists(path_101)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_100, session=score_manager._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_101, session=score_manager._session)
        title = 'Example Score 101'
        manager._add_metadatum('title', title)
        input_ = 'rm Example~Score~100~-~Example~Score~101 remove~2 q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(path_100)
        assert not os.path.exists(path_101)
    finally:
        if os.path.exists(path_100):
            shutil.rmtree(path_100)
        if os.path.exists(path_101):
            shutil.rmtree(path_101)
    assert not os.path.exists(path_100)
    assert not os.path.exists(path_101)