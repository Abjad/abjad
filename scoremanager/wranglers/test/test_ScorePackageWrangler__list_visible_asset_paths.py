# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ScorePackageWrangler__list_visible_asset_paths_01():
    r'''Abjad score packages directory.
    '''
    
    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.ScorePackageWrangler(session=session)
    
    package_names = [
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        ]

    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.abjad_score_packages_directory_path,
            package_name,
            )
        paths.append(path)

    # TODO: should be possible to set abjad_library=False
    result = wrangler._list_visible_asset_paths(
        abjad_library=True,
        abjad_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
