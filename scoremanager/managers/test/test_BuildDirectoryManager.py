# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_BuildDirectoryManager_01():

    string = 'scoremanager.scorepackages.red_example_score'
    manager = scoremanager.managers.BuildDirectoryManager(string)

    assert manager.filesystem_path == os.path.join(
        manager.configuration.score_manager_directory_path,
        'scorepackages', 
        'red_example_score', 
        'build',
        )
    assert manager._spaced_class_name == 'build directory manager'
