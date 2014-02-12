# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_DistributionDirectoryManager_01():

    string = 'scoremanager.scorepackages.red_example_score'
    manager = scoremanager.managers.DistributionDirectoryManager(string)

    assert manager.filesystem_path == os.path.join(
        manager.configuration.built_in_score_packages_directory_path,
        'red_example_score', 
        'distribution',
        )
    assert manager._spaced_class_name == 'distribution directory manager'
