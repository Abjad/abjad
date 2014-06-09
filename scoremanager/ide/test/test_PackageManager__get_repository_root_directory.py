# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_PackageManager__get_repository_root_directory_01():

    score_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        )
    manager = scoremanager.ide.PackageManager(
        path=score_path,
        session=score_manager._session,
        )

    repository_root_directory = manager._get_repository_root_directory()
    abjad_root_directory = manager._configuration.abjad_root_directory
    assert repository_root_directory == abjad_root_directory