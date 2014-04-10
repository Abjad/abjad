# -*- encoding: utf-8 -*-
import os
import pytest
pytest.skip("make 'Test Score 1' match 'Test Score 1'.")
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_remove_score_package_01():
    r'''Removes one score package.
    '''

    path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'test_score_1',
        )

    assert not os.path.exists(path)
    try:
        input_ = 'ssv new test~score~1 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=score_manager._session)
        title = 'Test Score 1'
        manager._add_metadatum('title', title)
        input_ = 'ssv rm Test~Score~1 remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)