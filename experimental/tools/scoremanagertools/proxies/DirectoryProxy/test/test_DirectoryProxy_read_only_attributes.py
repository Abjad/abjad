import os
from experimental import *


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_proxy = scoremanagertools.proxies.DirectoryProxy(directory_path)
    assert directory_proxy.path is not None
    # TODO: uncomment
    #assert directory_proxy.is_versioned


def test_DirectoryProxy_read_only_attributes_02():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    directory_path = score_manager_configuration.score_manager_tools_directory_path
    directory_proxy_1 = scoremanagertools.proxies.DirectoryProxy(directory_path)
    directory_proxy_2 = scoremanagertools.proxies.DirectoryProxy(directory_path)
    directory_proxy_3 = scoremanagertools.proxies.DirectoryProxy(
        score_manager_configuration.abjad_configuration.abjad_directory_path)

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
