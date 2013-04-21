import os
from experimental import *


def test_DirectoryProxy_read_only_attributes_01():
    '''Named directory proxy already written to disk.
    '''

    directory_proxy = scoremanagementtools.proxies.DirectoryProxy(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))
    assert directory_proxy.path_name is not None
    assert directory_proxy.is_versioned


def test_DirectoryProxy_read_only_attributes_02():

    directory_proxy_1 = scoremanagementtools.proxies.DirectoryProxy(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))
    directory_proxy_2 = scoremanagementtools.proxies.DirectoryProxy(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))
    directory_proxy_3 = scoremanagementtools.proxies.DirectoryProxy(os.environ.get('ABJAD'))

    assert     directory_proxy_1 == directory_proxy_2
    assert not directory_proxy_1 == directory_proxy_3
    assert not directory_proxy_2 == directory_proxy_3

    assert not directory_proxy_1 != directory_proxy_2
    assert     directory_proxy_1 != directory_proxy_3
    assert     directory_proxy_2 != directory_proxy_3
