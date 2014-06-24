# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetWrangler__list_storehouse_paths_01():
    r'''Lists example stylesheets directory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.StylesheetWrangler(session=session)

    paths = [
        wrangler._configuration.example_stylesheets_directory,
        ]

    result = wrangler._list_storehouse_paths(
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=False,
        library=False,
        user_score_packages=False,
        )

    assert result == paths


def test_StylesheetWrangler__list_storehouse_paths_02():
    r'''Lists example score package stylesheet directories.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.StylesheetWrangler(session=session)

    score_names = [
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        ]

    paths = []
    for score_name in score_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            score_name,
            'stylesheets',
            )
        paths.append(path)

    result = wrangler._list_storehouse_paths(
        abjad_material_packages_and_stylesheets=False,
        example_score_packages=True,
        library=False,
        user_score_packages=False,
        )

    assert result == paths