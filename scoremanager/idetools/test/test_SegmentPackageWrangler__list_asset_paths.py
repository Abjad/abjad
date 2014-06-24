# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_SegmentPackageWrangler__list_asset_paths_01():
    r'''Lists all segment packages resident in Abjad score packages.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.SegmentPackageWrangler(session=session)

    blue_segment_names = [
        'segment_01',
        'segment_02',
        ]

    red_segment_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]

    paths = []

    for segment_name in blue_segment_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            'blue_example_score',
            'segments',
            segment_name,
            )
        paths.append(path)

    for segment_name in red_segment_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            segment_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_material_packages_and_stylesheets=False,
        example_score_packages=True,
        library=False,
        user_score_packages=False,
        )

    assert result == paths