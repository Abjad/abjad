import os
from experimental import *


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH
    directory_proxy = scoremanagertools.proxies.DirectoryProxy(path)
    assert directory_proxy.path_name is not None
    # TODO: uncomment
    #assert directory_proxy.is_versioned


def test_DirectoryProxy_read_only_attributes_02():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH
    directory_proxy_1 = scoremanagertools.proxies.DirectoryProxy(path)
    directory_proxy_2 = scoremanagertools.proxies.DirectoryProxy(path)
    directory_proxy_3 = scoremanagertools.proxies.DirectoryProxy(os.environ.get('ABJAD'))

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
