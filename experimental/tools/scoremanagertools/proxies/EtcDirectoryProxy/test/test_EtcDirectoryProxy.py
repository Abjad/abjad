import os
from experimental import *


def test_EtcDirectoryProxy_01():

    etc_proxy = scoremanagertools.proxies.EtcDirectoryProxy('example_score_1')

    assert etc_proxy.directory_path == os.path.join(
        etc_proxy.configuration.scores_directory_path, 'example_score_1', 'etc')
    assert etc_proxy.source_file_name == \
        os.path.join(
            etc_proxy.configuration.score_manager_tools_directory_path,
            'proxies', 'EtcDirectoryProxy', 'EtcDirectoryProxy.py')
    assert etc_proxy._spaced_class_name == 'etc directory proxy'
