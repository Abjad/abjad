# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__list_storehouse_paths_01():
    r'''Abjad score package material directories.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)

    score_package_names = [
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        ]

    paths = []
    for score_package_name in score_package_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            score_package_name,
            'materials',
            )
        paths.append(path)

    result = wrangler._list_storehouse_paths(
        abjad_material_packages_and_stylesheets=False,
        example_score_packages=True,
        library=False,
        user_score_packages=False,
        )

    assert result == paths