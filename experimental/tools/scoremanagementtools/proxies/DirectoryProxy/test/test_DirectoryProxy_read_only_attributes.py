import os
from experimental import *


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    score_manager_configuration = scoremanagementtools.core.ScoreManagerConfiguration()
    path = score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH
    directory_proxy = scoremanagementtools.proxies.DirectoryProxy(path)
    assert directory_proxy.path_name is not None
    # TODO: uncomment
    #assert directory_proxy.is_versioned


def test_DirectoryProxy_read_only_attributes_02():

    score_manager_configuration = scoremanagementtools.core.ScoreManagerConfiguration()
    path = score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH
    directory_proxy_1 = scoremanagementtools.proxies.DirectoryProxy(path)
    directory_proxy_2 = scoremanagementtools.proxies.DirectoryProxy(path)
    directory_proxy_3 = scoremanagementtools.proxies.DirectoryProxy(os.environ.get('ABJAD'))

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
