# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ScorePackageManager_read_only_attributes_01():
    r'''Read-only public attributes.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    package_manager = scoremanager.managers.ScorePackageManager(string)

    assert isinstance(
        package_manager._segment_wrangler, 
        scoremanager.wranglers.SegmentPackageWrangler,
        )
    assert isinstance(
        package_manager._distribution_directory_manager, 
        scoremanager.managers.DirectoryManager,
        )
    assert isinstance(
        package_manager._build_directory_manager, 
        scoremanager.managers.DirectoryManager,
        )
    assert isinstance(
        package_manager._material_package_manager_wrangler,
        scoremanager.wranglers.MaterialPackageManagerWrangler,
        )
    assert isinstance(
        package_manager._material_package_wrangler,
        scoremanager.wranglers.MaterialPackageWrangler,
        )

    assert package_manager._get_annotated_title() == 'Red Example Score (2013)'
    assert package_manager._breadcrumb == 'Red Example Score (2013)'
    assert package_manager._get_metadatum('composer') is None
    assert package_manager._get_metadatum('title') == 'Red Example Score'
    assert package_manager._get_metadatum('year_of_completion') == 2013
