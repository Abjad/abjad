# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_DirectoryManager_read_only_attributes_01():
    r'''Named directory manager already written to disk.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_manager = scoremanagertools.managers.DirectoryManager(directory_path)
    assert directory_manager.filesystem_path is not None
    # TODO: uncomment soon
    #assert directory_manager._is_versioned()
