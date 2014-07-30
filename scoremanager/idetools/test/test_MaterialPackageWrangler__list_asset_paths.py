# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__list_asset_paths_01():
    r'''Red Example Score material packages.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)

    package_names = (
        'magic_numbers',
        'performer_inventory',
        'pitch_range_inventory',
        'tempo_inventory',
        'time_signatures',
        )
    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            )
        paths.append(path)
    package_names = (
        'articulation_handler',
        'dynamic_handler',
        'markup_inventory',
        'sargasso_measures',
        'talea_rhythm_maker',
        )
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            'blue_example_score',
            'materials',
            package_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_material_packages_and_stylesheets=False,
        example_score_packages=True,
        library=False,
        user_score_packages=False,
        )

    for path in paths:
        assert path in result
    assert len(paths) == len(result)