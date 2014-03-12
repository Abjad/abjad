# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_SegmentPackageWrangler__list_storehouse_paths_01():
    r'''Lists all Abjad score package segment directories.
    '''
    
    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.SegmentPackageWrangler(session=session)
    
    package_names = [
        'blue_example_score',
        'green_example_score',
        'red_example_score',
        ]

    paths = []
    for package_name in package_names:
        path = os.path.join(
            wrangler._configuration.abjad_score_packages_directory_path,
            package_name,
            'segments',
            )
        paths.append(path)

    result = wrangler._list_storehouse_paths(
        abjad_library=False,
        abjad_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
