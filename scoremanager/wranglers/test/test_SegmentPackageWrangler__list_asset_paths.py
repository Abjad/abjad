# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_SegmentPackageWrangler__list_asset_paths_01():
    r'''Lists all segment packages resident in Abjad score packages.
    '''

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.SegmentPackageWrangler(session=session)

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
            wrangler._configuration.example_score_packages_directory_path,
            'blue_example_score',
            'segments',
            segment_name,
            )
        paths.append(path)

    for segment_name in red_segment_names:
        path = os.path.join(
            wrangler._configuration.example_score_packages_directory_path,
            'red_example_score',
            'segments',
            segment_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_library=False,
        example_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths