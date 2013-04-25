import os
from experimental import *


def test_EtcDirectoryProxy_01():

    etc_proxy = scoremanagertools.proxies.EtcDirectoryProxy('example_score_1')

    assert etc_proxy.path == os.path.join(
        etc_proxy.configuration.SCORES_DIRECTORY_PATH, 'example_score_1', 'etc')
    assert etc_proxy.source_file_name == \
        os.path.join(
            etc_proxy.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
            'proxies', 'EtcDirectoryProxy', 'EtcDirectoryProxy.py')
    assert etc_proxy._spaced_class_name == 'etc directory proxy'
