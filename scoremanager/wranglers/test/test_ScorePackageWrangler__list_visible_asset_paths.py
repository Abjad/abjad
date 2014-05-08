# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work')
import os
from abjad import *
import scoremanager


def test_ScorePackageWrangler__list_visible_asset_paths_01():
    r'''Abjad score packages directory.
    '''

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.ScorePackageWrangler(session=session)

    package_names = [
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        ]

    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory_path,
            package_name,
            )
        paths.append(path)

    result = wrangler._list_visible_asset_paths()

    assert result == paths