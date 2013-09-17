# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_BuildDirectoryManager_01():

    manager = scoremanagertools.proxies.BuildDirectoryManager(
        'scoremanagertools.scorepackages.red_example_score')

    assert manager.filesystem_path == os.path.join(
        manager.configuration.score_manager_tools_directory_path,
        'scorepackages', 
        'red_example_score', 
        'exergue',
        )
    assert manager._spaced_class_name == 'build directory manager'
