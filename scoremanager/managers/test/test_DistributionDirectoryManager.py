# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_DistributionDirectoryManager_01():

    distribution_directory_manager = scoremanager.managers.DistributionDirectoryManager(
        'scoremanager.scorepackages.red_example_score')

    assert distribution_directory_manager.filesystem_path == os.path.join(
        distribution_directory_manager.configuration.built_in_score_packages_directory_path,
        'red_example_score', 'distribution')
    assert distribution_directory_manager._spaced_class_name == \
        'distribution directory manager'
