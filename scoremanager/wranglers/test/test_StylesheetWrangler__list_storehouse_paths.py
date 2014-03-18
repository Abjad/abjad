# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetWrangler__list_storehouse_paths_01():
    r'''Lists Abjad stylesheet library path.
    '''
    
    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.StylesheetWrangler(session=session)
    
    paths = [
        wrangler._configuration.abjad_stylesheets_directory_path,
        ]

    result = wrangler._list_storehouse_paths(
        abjad_library=True,
        abjad_score_packages=False,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths


def test_StylesheetWrangler__list_storehouse_paths_02():
    r'''Lists paths of Abjad score package stylesheet directories.
    '''
    
    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.StylesheetWrangler(session=session)
    
    score_names = [
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        ]

    paths = []
    for score_name in score_names:
        path = os.path.join(
            wrangler._configuration.abjad_score_packages_directory_path,
            score_name,
            'stylesheets',
            )
        paths.append(path)

    result = wrangler._list_storehouse_paths(
        abjad_library=False,
        abjad_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
