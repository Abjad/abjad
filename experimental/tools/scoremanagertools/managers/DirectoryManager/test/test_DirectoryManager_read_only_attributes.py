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
    #assert directory_manager.is_versioned()


def test_DirectoryManager_read_only_attributes_02():

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_manager_1 = scoremanagertools.managers.DirectoryManager(directory_path)
    directory_manager_2 = scoremanagertools.managers.DirectoryManager(directory_path)
    directory_manager_3 = scoremanagertools.managers.DirectoryManager(
        score_manager_configuration.abjad_configuration.abjad_directory_path)

    assert     directory_manager_1 == directory_manager_2
    assert not directory_manager_1 == directory_manager_3
    assert not directory_manager_2 == directory_manager_3

    assert not directory_manager_1 != directory_manager_2
    assert     directory_manager_1 != directory_manager_3
    assert     directory_manager_2 != directory_manager_3
