# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work again.')
import os
from abjad import *
import scoremanager
#score_manager = scoremanager.core.ScoreManager(is_test=True)
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_ScorePackageWrangler_rename_package_01():
    r'''Creates score package. Renames score package.
    '''

    path_100 = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score_100',
        )
    path_101 = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score_101',
        )

    with systemtools.FilesystemState(remove=[path_100, path_101]):
        input_ = 'new example~score~100 q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path_100)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path_100, session=score_manager._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        input_ = 'ren Example~Score~100 example_score_101 y q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(path_100)
        assert os.path.exists(path_101)