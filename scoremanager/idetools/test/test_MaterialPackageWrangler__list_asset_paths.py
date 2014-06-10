# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__list_asset_paths_01():
    r'''Abjad library material pcakages.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)

    package_names = [
        'example_articulation_handler',
        'example_dynamic_handler',
        'example_markup_inventory',
        'example_notes',
        'example_numbers',
        'example_pitch_range_inventory',
        'example_sargasso_measures',
        ]

    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.abjad_material_packages_directory,
            package_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_library=True,
        example_score_packages=False,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths


def test_MaterialPackageWrangler__list_asset_paths_02():
    r'''Red Example Score material library.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)

    package_names = [
        'instrumentation',
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        'time_signatures',
        ]

    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            )
        paths.append(path)
    path = os.path.join(
        wrangler._configuration.example_score_packages_directory,
        'blue_example_score',
        'materials',
        'sargasso_measures',
        )
    paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_library=False,
        example_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    for path in paths:
        assert path in result
    assert len(paths) == len(result)