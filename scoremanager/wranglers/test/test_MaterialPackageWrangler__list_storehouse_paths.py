# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__list_storehouse_paths_01():
    r'''Abjad library materials directory.
    '''
    
    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    
    paths = [
        wrangler._configuration.abjad_material_packages_directory_path,
        ]

    result = wrangler._list_storehouse_paths(
        abjad_library=True,
        abjad_score_packages=False,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths


def test_MaterialPackageWrangler__list_storehouse_paths_02():
    r'''Abjad score package material directories.
    '''
    
    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    
    score_package_names = [
        'blue_example_score',
        'green_example_score',
        'red_example_score',
        ]

    paths = []
    for score_package_name in score_package_names:
        path = os.path.join(
            wrangler._configuration.abjad_score_packages_directory_path,
            score_package_name,
            'materials',
            )
        paths.append(path)

    result = wrangler._list_storehouse_paths(
        abjad_library=False,
        abjad_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
