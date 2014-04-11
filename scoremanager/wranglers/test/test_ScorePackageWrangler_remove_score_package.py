# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_remove_score_package_01():
    r'''Removes one score package.
    '''

    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score_100',
        )

    assert not os.path.exists(path)
    try:
        input_ = 'ssv new test~score~100 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=score_manager._session)
        title = 'Test Score 100'
        manager._add_metadatum('title', title)
        input_ = 'ssv rm Test~Score~100 remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_ScorePackageWrangler_remove_score_package_02():
    r'''Removes range of score packages.
    '''

    path_100 = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score_100',
        )
    path_101 = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score_101',
        )

    assert not os.path.exists(path_100)
    try:
        input_ = 'ssv new test~score~100 new test~score~101 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path_100)
        assert os.path.exists(path_101)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_100, session=score_manager._session)
        title = 'Test Score 100'
        manager._add_metadatum('title', title)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_101, session=score_manager._session)
        title = 'Test Score 101'
        manager._add_metadatum('title', title)
        input_ = 'ssv rm Test~Score~100~-~Test~Score~101 remove~2 q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path_100)
        assert not os.path.exists(path_101)
    finally:
        write_cache = False
        if os.path.exists(path_100):
            shutil.rmtree(path_100)
            write_cache = True
        if os.path.exists(path_101):
            shutil.rmtree(path_101)
            write_cache = True
        if write_cache:
            score_manager.write_cache(prompt=False)
    assert not os.path.exists(path_100)
    assert not os.path.exists(path_101)