# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_DirectoryManager_read_only_attributes_01():
    r'''Named directory proxy already written to disk.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_proxy = scoremanagertools.managers.DirectoryManager(directory_path)
    assert directory_proxy.filesystem_path is not None
    # TODO: uncomment soon
    #assert directory_proxy.is_versioned()


def test_DirectoryManager_read_only_attributes_02():

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_proxy_1 = scoremanagertools.managers.DirectoryManager(directory_path)
    directory_proxy_2 = scoremanagertools.managers.DirectoryManager(directory_path)
    directory_proxy_3 = scoremanagertools.managers.DirectoryManager(
        score_manager_configuration.abjad_configuration.abjad_directory_path)

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
