# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work again.')
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=False)


def test_ScorePackageWrangler_rename_package_01():
    r'''Creates score package. Renames score package.
    '''

    path_100 = os.path.join(
        ide._configuration.user_score_packages_directory,
        'example_score_100',
        )
    path_101 = os.path.join(
        ide._configuration.user_score_packages_directory,
        'example_score_101',
        )

    with systemtools.FilesystemState(remove=[path_100, path_101]):
        input_ = 'new example~score~100 q'
        ide._run(input_=input_)
        assert os.path.exists(path_100)
        manager = scoremanager.idetools.ScorePackageManager
        manager = manager(path=path_100, session=ide._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        input_ = 'ren Example~Score~100 example_score_101 y q'
        ide._run(input_=input_)
        assert not os.path.exists(path_100)
        assert os.path.exists(path_101)