# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_DirectoryManager_read_only_attributes_01():
    r'''Named directory manager already written to disk.
    '''

    score_manager_configuration = scoremanager.core.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_directory_path
    directory_manager = scoremanager.managers.DirectoryManager(directory_path)
    assert directory_manager._filesystem_path is not None
