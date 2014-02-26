# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScorePackageManager_read_only_attributes_01():
    r'''Read-only public attributes.
    '''

    string = 'scoremanager.scores.red_example_score'
    filesystem_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
    package_manager = scoremanager.managers.ScorePackageManager(
        filesystem_path=filesystem_path)

    assert isinstance(
        package_manager._segment_package_wrangler, 
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
        package_manager._material_manager_wrangler,
        scoremanager.wranglers.MaterialManagerWrangler,
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
